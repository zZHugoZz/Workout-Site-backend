from sqlalchemy.ext.asyncio import AsyncSession


async def exec_update_stmt(update_stmt: any, session: AsyncSession) -> any:
    exec = await session.execute(update_stmt)
    await session.commit()
    updated_item = exec.scalars().first()
    return updated_item


async def exec_select_stmt(select_stmt: any, session: AsyncSession) -> any:
    exec = await session.execute(select_stmt)
    await session.commit()
    selected_item = exec.scalars().first()
    return selected_item


async def add_to_db(created_item, session: AsyncSession):
    session.add(created_item)
    await session.commit()
    await session.refresh(created_item)
