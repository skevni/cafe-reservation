from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        return await session.get(self.model, obj_id)

    async def get_all(self, session: AsyncSession):
        datas = await session.execute(select(self.model))
        return datas.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession, commit: bool = True,
        user: Optional[User] = None
    ):
        db_obj = self.model(**obj_in.dict())
        if hasattr(db_obj, 'user_id') and user is not None:
            db_obj.user_id = user.id
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        else:
            await session.flush()
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        if 'create_date' in update_data:
            del update_data['create_date']
        if 'close_date' in update_data:
            del update_data['close_date']

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get_active_for_investment(
            self,
            session: AsyncSession,
    ):
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )
        return objects.scalars().all()
