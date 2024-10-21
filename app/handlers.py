from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import logging

import keybords as kb
import database.requests as rq

router = Router()

logging.basicConfig(level=logging.INFO)

async def log_tasks(user_id):
    tasks = await rq.get_user_tasks(user_id)
    logging.info(f"Tasks for user {user_id}: {tasks}")

class Task(StatesGroup):
    description = State()
    date = State()
class Delete_Task(StatesGroup):
    id = State()
class Update_Task(StatesGroup):
    id = State()
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
    await message.answer('Введите задачу')

@router.message(Task.description)
async def add_task_third(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    tg_id = message.from_user.id
    task_date = data['date'] 
    task_description = data['description']  
    await rq.add_task(tg_id, task_date, task_description)  
    await state.clear()
    await message.answer('Задача добавлена',reply_markup=kb.main)

@router.message(F.text == 'Посмотреть задачи')
async def return_tasks(message: Message):
    tasks = await rq.get_user_tasks(message.from_user.id ) 
    if tasks:  
        task_strings = [
            f'#{index + 1}:\n{task.task_description} {"✅" if task.status else "❌"}\nДата: {task.task_date}'
            for index, task in enumerate(tasks)
        ]
        await message.answer("Ваши задачи:\n" + "\n".join(task_strings),reply_markup=kb.change_tasks) 
    else:
        await message.answer("У вас нет задач.",reply_markup=kb.main)

async def process_task_action(message: Message, state: FSMContext, action: str):
    await state.update_data(id=message.text) 
    data = await state.get_data()
    tasks = await rq.get_user_tasks(message.from_user.id)
    try:
        task_index = int(data['id']) - 1
        if task_index < 0 or task_index >= len(tasks):
            await message.answer("Некорректный индекс задачи.")
            return
        task_id = tasks[task_index].task_id
        if action == 'delete':
            await rq.delete_task(task_id)
            await message.answer("Задача удалена", reply_markup=kb.main)
        elif action == 'update':
            await rq.update_status(task_id)
            await message.answer("Задача отмечена выполненной", reply_markup=kb.main)
        await state.clear()
    except ValueError:
        await message.answer("Ошибка: неверный ID задачи.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

@router.message(F.text == 'Удалить задачу')
async def delete_task_first(message: Message, state: FSMContext):
    await state.set_state(Delete_Task.id)
    await message.answer('Введите номер задачи которую надо удалить')

@router.message(Delete_Task.id)
async def delete_task_second(message: Message, state: FSMContext):
    await process_task_action(message, state, 'delete')

@router.message(F.text == 'Отметить задачу выполненной')
async def update_status_first(message: Message, state: FSMContext):
    await state.set_state(Update_Task.id)
    await message.answer('Введите номер выполненной задачи')

@router.message(Update_Task.id)
async def update_status_second(message: Message, state: FSMContext):
    await process_task_action(message, state, 'update')

@router.message(F.text == 'В главное меню')
async def main_menu(message: Message):
     await message.answer('Добро пожаловать в планировщик задач', reply_markup=kb.main)