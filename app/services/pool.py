from __future__ import annotations

import asyncio
import secrets
from io import BytesIO
from pathlib import Path

import aiohttp
import openpyxl
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
    def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
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
    def _split_by_rooms(df: pd.DataFrame) -> list[pd.DataFrame]:
        df.replace("Студия", 0, inplace=True)
        df.replace("Да", True, inplace=True)
        df.replace("Нет", False, inplace=True)
        df["has_balcony"] = df["has_balcony"].astype("bool")
        df["rooms"] = df["rooms"].astype("int32")

        df.sort_values(by="rooms", inplace=True)

        dfs = [df[df["rooms"] == i] for i in range(df["rooms"].max() + 1)]
        return [i for i in dfs if not i.empty]

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
                    return -1, -1
                data = await response.json()
                if data["suggestions"]:
                    return (
                        data["suggestions"][0]["data"]["geo_lat"],
                        data["suggestions"][0]["data"]["geo_lon"],
                    )
                return -1, -1

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
        df = PoolService._rename_columns(df)
        dfs = PoolService._split_by_rooms(df)

        for i in range(len(dfs)):
            if dfs[i].empty:
                continue

            dfs[i].drop_duplicates(inplace=True)

            addresses = dfs[i]["address"].to_list()
            unique_addresses = list(set(addresses))

            tasks = [PoolService._convert_address(address) for address in unique_addresses]
            results = await asyncio.gather(*tasks)
            addresses_dict = dict(zip(unique_addresses, results))

            dfs[i]["lat"] = dfs[i]["address"].map(addresses_dict).apply(lambda x: x[0])
            dfs[i]["lon"] = dfs[i]["address"].map(addresses_dict).apply(lambda x: x[1])
            dfs[i] = dfs[i][(dfs[i]["lat"] != -1) & (dfs[i]["lon"] != -1)]

            if name is None:
                name = dfs[i]["address"].iloc[0]

        sub_queries = await PoolService._convert_dfs_to_model(dfs)

        query = QueryCreate(
            name=name,
            sub_queries=sub_queries,
            created_by=user,
            updated_by=user,
            input_file=f"{config.STORAGE_ENDPOINT}/{config.STORAGE_BUCKET_NAME}/{filename}.xlsx",
        )

        query_db = await QueryService.create(db=db, model=query)

        for _ in range(len(query_db.sub_queries)):
            query_db.sub_queries.sort(key=lambda x: x.input_apartments[0].rooms)

        return query_db

    @staticmethod
    async def export(db: AsyncSession, guid: UUID4, include_adjustments: bool, split_by_lists: bool, user: UUID4):
        query = await QueryService.get(db=db, guid=guid)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data"
        ws["A1"] = "Местоположение"
        ws["B1"] = "Количество комнат"
        ws["C1"] = "Сегмент"
        ws["D1"] = "Этажность дома"
        ws["E1"] = "Материал стен"
        ws["F1"] = "Этаж расположения"
        ws["G1"] = "Площадь квартиры, кв.м"
        ws["H1"] = "Площадь кухни, кв.м"
        ws["I1"] = "Наличие балкона/лоджии"
        ws["J1"] = "Удаленность от станции метро, мин. пешком"
        ws["K1"] = "Состояние"
        ws["L1"] = "Цена за кв.м"
        ws["M1"] = "Цена"

        for col in ws.iter_cols(min_row=1, max_row=1, min_col=1, max_col=11):
            for cell in col:
                cell.fill = openpyxl.styles.PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
                cell.alignment = openpyxl.styles.Alignment(wrap_text=True)
                # cell.border = openpyxl.styles.Border(right=openpyxl.styles.Side(border_style='thin'))
                cell.border = openpyxl.styles.Border(right=openpyxl.styles.Side(border_style="thick"))

        for row in ws.iter_rows(min_row=1, max_row=1, min_col=1, max_col=11):
            for cell in row:
                cell.border = openpyxl.styles.Border(
                    top=openpyxl.styles.Side(border_style="thick"), bottom=openpyxl.styles.Side(border_style="thick")
                )

        ws.column_dimensions["A"].width = 17.5
        ws.column_dimensions["B"].width = 13.5
        ws.column_dimensions["C"].width = 23
        ws.column_dimensions["D"].width = 15
        ws.column_dimensions["E"].width = 15
        ws.column_dimensions["F"].width = 15
        ws.column_dimensions["G"].width = 15.5
        ws.column_dimensions["H"].width = 15.5
        ws.column_dimensions["I"].width = 15.5
        ws.column_dimensions["J"].width = 15
        ws.column_dimensions["K"].width = 15
        ws.column_dimensions["L"].width = 15
        ws.column_dimensions["M"].width = 15

        Path(__file__).parent

        for i in range(len(query.sub_queries)):
            sub_query = query.sub_queries[i]
            for j in range(2, len(sub_query.input_apartments) + 2):
                input_apartment = sub_query.input_apartments[j]
                ws[f"A{i}"] = input_apartment.address
                ws[f"B{i}"] = input_apartment.rooms
                ws[f"C{i}"] = input_apartment.segment
                ws[f"D{i}"] = input_apartment.floors
                ws[f"E{i}"] = input_apartment.walls
                ws[f"F{i}"] = input_apartment.floor
                ws[f"G{i}"] = input_apartment.apartment_area
                ws[f"H{i}"] = input_apartment.kitchen_area
                ws[f"I{i}"] = input_apartment.has_balcony
                ws[f"J{i}"] = input_apartment.distance_to_metro
                ws[f"K{i}"] = input_apartment.quality
                ws[f"L{i}"] = input_apartment.m2price
                ws[f"M{i}"] = input_apartment.price

        # wb.save(cur_dir / 'data.xlsx')
