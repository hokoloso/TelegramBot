from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить задачу'),KeyboardButton(text='Посмотреть задачи')]
], resize_keyboard=True)