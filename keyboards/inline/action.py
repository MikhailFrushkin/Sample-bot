from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from keyboards.default.menu import second_menu
from loader import bot

inline_kb = InlineKeyboardMarkup()
url_button = InlineKeyboardButton(text='Анкета',
                                  callback_data='check_1',
                                  url='https://docs.google.com/forms/d/e/1FAIpQLScOBgEuuv7rj7wfOBJEAFIjBhztFLs6R4KbgHv4fryINAo66Q/viewform')
inline_kb.add(url_button)
