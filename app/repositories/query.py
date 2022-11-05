from collections import namedtuple
from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Adjustment, Apartment, Query, SubQuery
from app.models import ApartmentCreate, QueryCreate, QueryCreateBaseApartment, QueryCreateUserApartments, QueryPatch


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
    ) -> None:
        for analog in analogs.guids:
            await db.execute(
                update(Apartment).where(Apartment.guid == analog).values({"selected_analogs_guid": subguid})
            )
            await db.commit()

    async def _nameddict(typename: str, keys: list[str | tuple]) -> dict:
        _class_template = f"""class {typename}(dict):\n    def __init__(self, *args, **kwargs):\n        super().__init__()\n        for key in {keys}:\n            self[key] = None\n        if args and len(args) == len(self.keys()):\n            self.update(zip(self.keys(), args))"""
        namespace = dict(__name__=f'nameddict_{typename}')
        exec(_class_template, namespace)
        return namespace[typename]

    async def _find_match(adjustment: dict, key: int, value: int) -> int | float:
        for k, v in adjustment.items():
            if k[0] < key <= k[1]:
                for i, j in v.items():
                    if i[0] < value <= i[1]:
                        return j

    @staticmethod
    async def get_adj_and_price(adj_type: str, calculating_object_value: int | str, analog_value: int | str, analog_price: int) -> tuple[float, int]:
        Floor = _nameddict("Floor", ["first", "middle", "last"])
        AptArea = _nameddict("AptArea", [(0, 30), (30, 50), (50, 65), (65, 90), (90, 120), (120, 1000)])
        KitchenArea = _nameddict("KitchenArea", [(0, 7), (7, 10), (10, 15)])
        HasBalcony = _nameddict("HasBalcony", [True, False])
        ToMetro = _nameddict("ToMetro", [(0, 5), (5, 10), (10, 15), (15, 30), (30, 60), (60, 90)])
        RepairType = _nameddict("RepairType", ["without_repair", "municipal", "modern"])

        floor = {
            'first':  Floor(0, -.07, -.031),
            'middle': Floor(.075, 0, .042),
            'last':   Floor(-.032, -.04, 0),
        }
        apt_area = {
            (0, 30):     AptArea(0, .06, .14, .21, .28, .31),
            (30, 50):    AptArea(-.06, 0, .07, .14, .21, .24),
            (50, 65):    AptArea(-.12, -.07, 0, .06, .13, .16),
            (65, 90):    AptArea(-.17, -.12, -.06, 0, .06, .09),
            (90, 120):   AptArea(-.22, -.17, -.11, -.06, 0, .03),
            (120, 1000): AptArea(-.24, -.19, -.13, -.08, -.03, 0),
        }
        kitchen_area = {
            (0, 7):   KitchenArea(0, -.029, -.083),
            (7, 10):  KitchenArea(.03, 0, -.055),
            (10, 15): KitchenArea(.09, .058, 0),
        }
        has_balcony = {
            True:  HasBalcony(0, -.05),
            False: HasBalcony(.053 , 0),
        }
        to_metro = {
            (0, 5):   ToMetro(0, .07, .12, .17, .24, .29),
            (5, 10):  ToMetro(-.07, 0, .04, .9, .15, .20),
            (10, 15): ToMetro(-.11, -.04, 0, .05, .11, .15),
            (15, 30): ToMetro(-.15, -.08, -.05, 0, .06, .1),
            (30, 60): ToMetro(-.19, -.13, -.1, -.06, 0, .04),
            (60, 90): ToMetro(-.22, -.17, -.13, -.09, -.04, 0),
        }
        repair_type = {
            'without_repair': RepairType(0, -13400, -20100),
            'municipal':      RepairType(13400, 0, -6700),
            'modern':         RepairType(20100, 6700, 0),
        }

        adjustments = dict(floor=floor, apt_area=apt_area, kitchen_area=kitchen_area, has_balcony=has_balcony, to_metro=to_metro, repair_type=repair_type)
        match adj_type:
            case 'trade':
                adj = -0.045
            case 'apt_area' | 'kitchen_area' | 'to_metro':
                adj = _find_match(adjustments[adj_type], calculating_object_value, analog_value)
            case 'floor' | 'has_balcony' | 'repair_type':
                adj = adjustments[adj_type][calculating_object_value][analog_value]
            case _:
                raise ValueError(f'Неизвестный тип аналога: {adj_type}. Доступные типы: {"trade, " + ", ".join(adjustments.keys())}')
        if adj_type == 'repair_type':
            price = analog_price + adj
        else:
            price = analog_price * (1 + adj)
        return adj, int(price)

    @staticmethod
    async def calculate_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4) -> None:
        subquery = await QueryRepository.get_subquery(db, subguid)
        standart_object = subquery.standart_object
        analogs = subquery.analogs

        for analog in analogs:
            if standart_object.floor == 1:
                pass
            elif standart_object.floor == standart_object.floors:
                pass
            else:
                pass