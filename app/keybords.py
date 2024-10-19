from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить задачу'),KeyboardButton(text='Посмотреть задачи')]
], resize_keyboard=True)
change_tasks = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить задачу'),KeyboardButton(text='Отметить задачу выполненной')],
    [KeyboardButton(text='Удалить задачу'),KeyboardButton(text='В главное меню')]
], resize_keyboard=True)