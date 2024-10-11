from database.models import async_session
from database.models import User,Task
from sqlalchemy import select,update,delete

async def set_user(tg_id):
    async with async_session() as session:
        user= await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_task(tg_id,taskdate,taskdescription):
    async with async_session() as session:
        user_id_result = await session.execute(
            select(User.id).filter(User.tg_id == tg_id)
        )
        userid = user_id_result.scalar()
        session.add(Task(user_id=userid,task_description=taskdescription,status=False,task_date=taskdate))
        await session.commit()

