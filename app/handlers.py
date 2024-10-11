from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keybords as kb
import database.requests as rq

router = Router()

class Task(StatesGroup):
    description = State()
    date = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в планировщик задач', reply_markup=kb.main)

@router.message(F.text == 'Добавить задачу')
async def add_task_first(message: Message, state: FSMContext):
    await state.set_state(Task.date)
    await message.answer('Введите дату и время выполнения задачи в формате ДД.ММ.ГГГГ ЧЧ:ММ')

@router.message(Task.date)
async def add_task_second(message: Message, state: FSMContext):
    await state.update_data(date=message.text)  
    await state.set_state(Task.description)
    await message.answer('Введите описание задачи')

@router.message(Task.description)
async def add_task_third(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    tg_id = message.from_user.id
    task_date = data['date'] 
    task_description = data['description']  
    await rq.add_task(tg_id, task_date, task_description)  
    await message.answer('Задача добавлена',reply_markup=kb.main)