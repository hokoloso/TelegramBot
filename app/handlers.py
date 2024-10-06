from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

import database.requests as rq

router = Router()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в планировщик задач')