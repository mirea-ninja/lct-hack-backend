from __future__ import annotations

from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Apartment, Query, SubQuery
from app.models import (
    AdjustmentCreate,
    ApartmentCreate,
    QueryCreate,
    QueryCreateBaseApartment,
    QueryCreateUserApartments,
    QueryPatch,
)
from app.repositories.adjustment import AdjustmentRepository


class QueryRepository:
    @staticmethod
    async def create(db: AsyncSession, model: QueryCreate) -> Query:
        query = Query(
            name=model.name,
            input_file=model.input_file,
            sub_queries=list(),
            created_by=model.created_by,
            updated_by=model.updated_by,
        )
        for sub_query in model.sub_queries:
            sub_query_object = SubQuery(
                input_apartments=[Apartment(**apartment.dict()) for apartment in sub_query.input_apartments],
            )
            query.sub_queries.append(sub_query_object)
        db.add(query)
        await db.commit()
        await db.refresh(query)
        return query

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Query]:
        res = await db.execute(select(Query).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Query:
        res = await db.execute(select(Query).where(Query.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, user: UUID4, model: QueryCreate) -> Query:
        query = await QueryRepository.get(db, guid)

        if query is None:
            raise HTTPException(404, "Запрос не найден")

        await db.execute(update(Query).where(Query.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(query)

        return query

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, user: UUID4, model: QueryPatch) -> Query:
        query = await QueryRepository.get(db, guid)

        if query is None:
            raise HTTPException(404, "Запрос не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Query).where(Query.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(query)

        return query

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(Query).where(Query.guid == guid))
        await db.commit()

    @staticmethod
    async def get_subquery(db: AsyncSession, subguid: UUID4) -> SubQuery:
        res = await db.execute(select(SubQuery).where(SubQuery.guid == subguid).limit(1))
        return res.scalar()

    @staticmethod
    async def set_base(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, stantart_object: QueryCreateBaseApartment
    ) -> Apartment:
        await db.execute(
            update(Apartment).where(Apartment.guid == stantart_object.guid).values({"standart_object_guid": subguid})
        )
        await db.commit()
        res = await db.execute(select(Apartment).where(Apartment.guid == stantart_object.guid).limit(1))
        return res.scalar()

    @staticmethod
    async def get_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4) -> List[Apartment]:
        subquery = await QueryRepository.get_subquery(db, subguid)
        if len(subquery.analogs) < 5:
            raise HTTPException(503, "Недостаточно аналогов")
        return subquery.analogs

    @staticmethod
    async def create_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4, analogs: List[ApartmentCreate]) -> None:
        subquery = await QueryRepository.get_subquery(db, subguid)
        db_analogs = [Apartment(**apartment.dict()) for apartment in analogs]
        subquery.analogs = db_analogs
        await db.commit()
        await db.refresh(subquery)

    @staticmethod
    async def set_analogs(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, analogs: QueryCreateUserApartments
    ) -> SubQuery:
        for analog in analogs.guids:
            await db.execute(
                update(Apartment).where(Apartment.guid == analog).values({"selected_analogs_guid": subguid})
            )
        await db.commit()
        subquery = await QueryRepository.get_subquery(db, subguid)
        return subquery

    @staticmethod
    async def _nameddict(typename: str, keys: list[str | tuple]) -> str:
        _class_template = f"""class {typename}(dict):\n    def __init__(self, *args, **kwargs):\n        super().__init__()\n        for key in {keys}:\n            self[key] = None\n        if args and len(args) == len(self.keys()):\n            self.update(zip(self.keys(), args))"""
        namespace = dict(__name__=f"nameddict_{typename}")
        exec(_class_template, namespace)
        return namespace[typename]

    @staticmethod
    async def _find_match(adjustment: dict, key: int, value: int) -> int | float:
        for k, v in adjustment.items():
            if k[0] < key <= k[1]:
                for i, j in v.items():
                    if i[0] < value <= i[1]:
                        return j

    @staticmethod
    async def get_adj_and_price(
        adj_type: str, calculating_object_value: int | str, analog_value: int | str, analog_price: float
    ) -> tuple[float, int]:
        Floor = await QueryRepository._nameddict("Floor", ["first", "middle", "last"])
        AptArea = await QueryRepository._nameddict(
            "AptArea", [(0, 30), (30, 50), (50, 65), (65, 90), (90, 120), (120, 1000)]
        )
        KitchenArea = await QueryRepository._nameddict("KitchenArea", [(0, 7), (7, 10), (10, 15)])
        HasBalcony = await QueryRepository._nameddict("HasBalcony", [True, False])
        ToMetro = await QueryRepository._nameddict("ToMetro", [(0, 5), (5, 10), (10, 15), (15, 30), (30, 60), (60, 90)])
        RepairType = await QueryRepository._nameddict("RepairType", ["without_repair", "municipal", "modern"])

        floor = {
            "first": Floor(0, -0.07, -0.031),
            "middle": Floor(0.075, 0, 0.042),
            "last": Floor(-0.032, -0.04, 0),
        }
        apt_area = {
            (0, 30): AptArea(0, 0.06, 0.14, 0.21, 0.28, 0.31),
            (30, 50): AptArea(-0.06, 0, 0.07, 0.14, 0.21, 0.24),
            (50, 65): AptArea(-0.12, -0.07, 0, 0.06, 0.13, 0.16),
            (65, 90): AptArea(-0.17, -0.12, -0.06, 0, 0.06, 0.09),
            (90, 120): AptArea(-0.22, -0.17, -0.11, -0.06, 0, 0.03),
            (120, 1000): AptArea(-0.24, -0.19, -0.13, -0.08, -0.03, 0),
        }
        kitchen_area = {
            (0, 7): KitchenArea(0, -0.029, -0.083),
            (7, 10): KitchenArea(0.03, 0, -0.055),
            (10, 15): KitchenArea(0.09, 0.058, 0),
        }
        has_balcony = {
            True: HasBalcony(0, -0.05),
            False: HasBalcony(0.053, 0),
        }
        to_metro = {
            (0, 5): ToMetro(0, 0.07, 0.12, 0.17, 0.24, 0.29),
            (5, 10): ToMetro(-0.07, 0, 0.04, 0.9, 0.15, 0.20),
            (10, 15): ToMetro(-0.11, -0.04, 0, 0.05, 0.11, 0.15),
            (15, 30): ToMetro(-0.15, -0.08, -0.05, 0, 0.06, 0.1),
            (30, 60): ToMetro(-0.19, -0.13, -0.1, -0.06, 0, 0.04),
            (60, 90): ToMetro(-0.22, -0.17, -0.13, -0.09, -0.04, 0),
        }
        repair_type = {
            "without_repair": RepairType(0, -13400, -20100),
            "municipal": RepairType(13400, 0, -6700),
            "modern": RepairType(20100, 6700, 0),
        }

        adjustments = dict(
            floor=floor,
            apt_area=apt_area,
            kitchen_area=kitchen_area,
            has_balcony=has_balcony,
            to_metro=to_metro,
            repair_type=repair_type,
        )

        if adj_type == "trade":
            adj = -0.045
        elif adj_type == "apt_area" or adj_type == "kitchen_area" or adj_type == "to_metro":
            adj = await QueryRepository._find_match(adjustments[adj_type], calculating_object_value, analog_value)
        elif adj_type == "floor" or adj_type == "repair_type" or adj_type == "has_balcony":
            adj = adjustments[adj_type][calculating_object_value][analog_value]

        if adj_type == "repair_type":
            price = analog_price + adj
        else:
            price = analog_price * (1 + adj)
        return adj, int(price)

    @staticmethod
    async def calculate_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4) -> Query:
        subquery = await QueryRepository.get_subquery(db, subguid)
        standart_object = subquery.standart_object
        standart_object_m2price = 0
        analogs = subquery.selected_analogs
        repair_type = {
            "без отделки": "without_repair",
            "муниципальный ремонт": "municipal",
            "современная отделка": "modern",
        }
        for analog in analogs:
            if standart_object.floor == 1:
                standart_object_floor = "first"
            elif standart_object.floor == standart_object.floors:
                standart_object_floor = "last"
            else:
                standart_object_floor = "middle"

            if analog.floor == 1:
                analog_object_floor = "first"
            elif analog.floor == standart_object.floors:
                analog_object_floor = "last"
            else:
                analog_object_floor = "middle"

            trade, price_trade = await QueryRepository.get_adj_and_price("trade", 0, 0, float(analog.m2price))
            floor, price_floor = await QueryRepository.get_adj_and_price(
                "floor", standart_object_floor, analog_object_floor, price_trade
            )
            apt_area, price_area = await QueryRepository.get_adj_and_price(
                "apt_area", standart_object.apartment_area, analog.apartment_area, price_floor
            )
            kitchen_area, price_kitchen_area = await QueryRepository.get_adj_and_price(
                "kitchen_area", standart_object.kitchen_area, analog.kitchen_area, price_area
            )
            has_balcony, price_balcony = await QueryRepository.get_adj_and_price(
                "has_balcony", standart_object.has_balcony, analog.has_balcony, price_kitchen_area
            )
            distance_to_metro, price_metro = await QueryRepository.get_adj_and_price(
                "to_metro", standart_object.distance_to_metro, analog.distance_to_metro, price_balcony
            )
            quality, price_final = await QueryRepository.get_adj_and_price(
                "repair_type",
                repair_type[standart_object.quality.lower()],
                repair_type[analog.quality.lower()],
                price_metro,
            )
            standart_object_m2price += analog.m2price
            model = AdjustmentCreate(
                trade=trade,
                floor=floor,
                apt_area=apt_area,
                kitchen_area=kitchen_area,
                has_balcony=has_balcony,
                distance_to_metro=distance_to_metro,
                quality=quality,
                price_trade=price_trade,
                price_floor=price_floor,
                price_area=price_area,
                price_kitchen=price_kitchen_area,
                price_balcony=price_balcony,
                price_metro=price_metro,
                price_final=price_final,
            )
            adjustment = await AdjustmentRepository.create(db, guid, subguid, model)
            analog.adjustment = adjustment
        standart_object.m2price = standart_object_m2price
        standart_object.price = standart_object_m2price * standart_object.apartment_area
        await db.commit()
        query = await QueryRepository.get(db, guid)
        return query

    @staticmethod
    async def calculate_pool(db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4) -> Query:
        subquery = await QueryRepository.get_subquery(db, subguid)
        standart_object = subquery.standart_object
        input_apartments = subquery.input_apartments
        repair_type = {
            "без отделки": "without_repair",
            "муниципальный ремонт": "municipal",
            "современный ремонт": "modern",
        }
        for input_apartment in input_apartments:
            if input_apartment.floor == 1:
                input_apartment_floor = "first"
            elif input_apartment.floor == input_apartment.floors:
                input_apartment_floor = "last"
            else:
                input_apartment_floor = "middle"

            if standart_object.floor == 1:
                standart_object_floor = "first"
            elif standart_object.floor == standart_object.floors:
                standart_object_floor = "last"
            else:
                standart_object_floor = "middle"

            trade, price_trade = await QueryRepository.get_adj_and_price("trade", 0, 0, float(input_apartment.m2price))
            floor, price_floor = await QueryRepository.get_adj_and_price(
                "floor", input_apartment_floor, standart_object_floor, price_trade
            )
            apt_area, price_area = await QueryRepository.get_adj_and_price(
                "apt_area", input_apartment.apartment_area, standart_object.apartment_area, price_floor
            )
            kitchen_area, price_kitchen_area = await QueryRepository.get_adj_and_price(
                "kitchen_area", input_apartment.kitchen_area, standart_object.kitchen_area, price_area
            )
            has_balcony, price_balcony = await QueryRepository.get_adj_and_price(
                "has_balcony", input_apartment.has_balcony, standart_object.has_balcony, price_kitchen_area
            )
            distance_to_metro, price_metro = await QueryRepository.get_adj_and_price(
                "to_metro", input_apartment.distance_to_metro, standart_object.distance_to_metro, price_balcony
            )
            quality, price_final = await QueryRepository.get_adj_and_price(
                "repair_type",
                repair_type[input_apartment.quality.lower()],
                repair_type[standart_object.quality.lower()],
                price_metro,
            )

            model = AdjustmentCreate(
                trade=trade,
                floor=floor,
                apt_area=apt_area,
                kitchen_area=kitchen_area,
                has_balcony=has_balcony,
                distance_to_metro=distance_to_metro,
                quality=quality,
                price_trade=price_trade,
                price_floor=price_floor,
                price_area=price_area,
                price_kitchen=price_kitchen_area,
                price_balcony=price_balcony,
                price_metro=price_metro,
                price_final=price_final,
            )
            input_apartment.m2price = (
                (price_final - float(standart_object.m2price)) * 100 / float(standart_object.m2price)
            )
            input_apartment.price = (
                (price_final - float(standart_object.m2price)) * 100 / float(standart_object.m2price)
            ) * standart_object.apartment_area
            adjustment = await AdjustmentRepository.create(db, guid, subguid, model)
            input_apartment.adjustment = adjustment
        await db.commit()
        query = await QueryRepository.get(db, guid)
        return query
