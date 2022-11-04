from __future__ import annotations

import secrets
from io import BytesIO

import aiohttp
import pandas as pd
from fastapi import UploadFile
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.models import ApartmentCreate, QueryCreate, QueryGet, SubQueryCreate
from app.services.query import QueryService
from app.storage import get_s3_client


async def send_file(file: bytes, filename: str) -> str:
    async with get_s3_client() as client:
        await client.put_object(
            Bucket=config.STORAGE_BUCKET_NAME,
            Key=f"{filename}",
            Body=file,
        )
    return f"{config.STORAGE_ENDPOINT}/{config.STORAGE_BUCKET_NAME}/{filename}"


class PoolService:
    @staticmethod
    async def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(
            columns={
                "Местоположение": "address",
                "Количество комнат": "rooms",
                "Сегмент (Новостройка, современное жилье, старый жилой фонд)": "segment",
                "Этажность дома": "floors",
                "Материал стен (Кипич, панель, монолит)": "walls",
                "Этаж расположения": "floor",
                "Площадь квартиры, кв.м": "apartment_area",
                "Площадь кухни, кв.м": "kitchen_area",
                "Наличие балкона/лоджии": "has_balcony",
                "Удаленность от станции метро, мин. пешком": "distance_to_metro",
                "Состояние (без отделки, муниципальный ремонт, с современная отделка)": "quality",
            }
        )

    @staticmethod
    async def _split_by_rooms(df: pd.DataFrame) -> list[pd.DataFrame]:
        df.replace("Студия", 0, inplace=True)
        df.replace("Да", True, inplace=True)
        df.replace("Нет", False, inplace=True)
        df["has_balcony"] = df["has_balcony"].astype("bool")
        df["rooms"] = df["rooms"].astype("int32")
        return [df[df["rooms"] == i] for i in range(len(df["rooms"].value_counts()))]

    @staticmethod
    async def _convert_address(address: str) -> tuple[float, float]:
        url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
        headers = {
            "Authorization": f"Token {config.BACKEND_DADATA_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json={"query": address},
            ) as response:
                if response.status != 200:
                    return 0, 0
                data = await response.json()
                if data["suggestions"]:
                    return (
                        data["suggestions"][0]["data"]["geo_lat"],
                        data["suggestions"][0]["data"]["geo_lon"],
                    )
                return 0, 0

    @staticmethod
    async def _convert_dfs_to_model(dfs: list[pd.DataFrame]) -> list[SubQueryCreate]:
        sub_queries = []
        for df in dfs:
            to_dict = df.to_dict(orient="records")
            apartments = [ApartmentCreate(**apartment) for apartment in to_dict]
            sub_queries.append(SubQueryCreate(input_apartments=apartments))
        return sub_queries

    @staticmethod
    async def _create_random_name() -> str:
        return secrets.token_hex(8)

    @staticmethod
    async def create(db: AsyncSession, user: UUID4, name: str, file: UploadFile) -> QueryGet:
        read_file = await file.read()
        filename = await PoolService._create_random_name()
        await send_file(file=read_file, filename=filename)

        df = pd.read_excel(BytesIO(read_file))
        df = await PoolService._rename_columns(df)
        dfs = await PoolService._split_by_rooms(df)

        if name is None:
            name = df.at[0, "address"]

        sub_queries = await PoolService._convert_dfs_to_model(dfs)

        query = QueryCreate(
            name=name,
            sub_queries=sub_queries,
            created_by=user,
            updated_by=user,
            input_file=f"{config.STORAGE_ENDPOINT}/{config.STORAGE_BUCKET_NAME}/{filename}.xlsx",
        )

        query_db = await QueryService.create(db=db, model=query)
        return query_db

    @staticmethod
    async def get_file(db: AsyncSession, query_id: UUID4):
        pass
