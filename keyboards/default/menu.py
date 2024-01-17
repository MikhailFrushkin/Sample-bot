from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import video_links, ADMINS
from data.db import User

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🔙Назад')],
], resize_keyboard=True)


def create_lesson_keyboard(lesson, user_id=None):
    user = User.get(User.user_id == user_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    if lesson == 4 and user.check_1 is False:
        markup.insert(KeyboardButton(text=f'📝ХОЧУ НА РАЗБОР'))
    elif lesson == 6 and user.check_2 is False:
        markup.insert(KeyboardButton(text=f'🚶🏼‍♀️ИДУ НА РАЗБОР'))
    elif str(lesson) in video_links:
        button_text = f"▶️Просмотреть {lesson} урок"
        markup.insert(KeyboardButton(text=button_text))
    if lesson > 1:
        markup.insert(KeyboardButton(text='🎬Доступные уроки'))
    if user.check_1 or user.check_2:
        markup.insert(KeyboardButton(text='👀Отзывы'))
        markup.insert(KeyboardButton(text='📕Анкета'))
    if str(user_id) in ADMINS:
        markup.insert(KeyboardButton(text='📊Статистика'))
    return markup
