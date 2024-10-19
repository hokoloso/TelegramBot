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
        user_id_result = await session.execute(select(User.id).filter(User.tg_id == tg_id))
        userid = user_id_result.scalar()
        session.add(Task(user_id=userid,task_description=taskdescription,status=False,task_date=taskdate))
        await session.commit()

async def get_user_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.id
    
async def get_user_tasks(tg_id):
    async with async_session() as session:
        user_id = await get_user_id(tg_id)
        result = await session.scalars(select(Task).where(Task.user_id == user_id)) 
        return result.all() 

async def delete_task(task_id):
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.task_id==task_id))
        await session.commit()