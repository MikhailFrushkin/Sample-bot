from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(row_width=2)
menu.insert(KeyboardButton('Найти сеты'))

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)

menu_admin = ReplyKeyboardMarkup(row_width=2)
menu_admin.insert(KeyboardButton('Найти сеты'))

