from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from keyboards.default.menu import second_menu
from loader import bot

price = InlineKeyboardMarkup(row_width=1)

price.insert(InlineKeyboardButton(text='0-500 руб.', callback_data='500'))
price.insert(InlineKeyboardButton(text='501-1000 руб.', callback_data='1000'))
price.insert(InlineKeyboardButton(text='1001-1500 руб.', callback_data='1500'))
price.insert(InlineKeyboardButton(text='от 1500 руб.', callback_data='2000'))
price.insert(InlineKeyboardButton(text='Любая цена', callback_data='0'))


nums = InlineKeyboardMarkup(row_width=1)
nums.insert(InlineKeyboardButton(text='5', callback_data='5'))
nums.insert(InlineKeyboardButton(text='10', callback_data='10'))
nums.insert(InlineKeyboardButton(text='15', callback_data='15'))
nums.insert(InlineKeyboardButton(text='20', callback_data='20'))


button_states = {'button1': True, 'button2': True, 'button3': True, 'button4': True}


def get_inline_menu():
    check_mark = '✅'
    cross_mark = '❌'

    button1_text = f'{check_mark} Суши Восток' if button_states['button1'] else f'{cross_mark} Суши Восток'
    button2_text = f'{check_mark} Империя' if button_states['button2'] else f'{cross_mark} Империя'
    button3_text = f'{check_mark} Японский домик' if button_states['button3'] else f'{cross_mark} Японский домик'
    button4_text = f'{check_mark} Суши-маке' if button_states['button4'] else f'{cross_mark} Суши-маке'
    button5_text = f'OK'

    button1 = types.InlineKeyboardButton(
        text=button1_text,
        callback_data='button1'
    )
    button2 = types.InlineKeyboardButton(
        text=button2_text,
        callback_data='button2'
    )
    button3 = types.InlineKeyboardButton(
        text=button3_text,
        callback_data='button3'
    )
    button4 = types.InlineKeyboardButton(
        text=button4_text,
        callback_data='button4'
    )
    ok = types.InlineKeyboardButton(
        text=button5_text,
        callback_data='ok'
    )

    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(button1, button2, button3, button4, ok)
    return inline_keyboard


# Функция для обновления иконки кнопки
async def update_button_icon(message, button):
    inline_menu = get_inline_menu()
    await bot.edit_message_reply_markup(
        message.chat.id,
        message.message_id,
        reply_markup=inline_menu
    )


# Отправка сообщения с инлайн-меню
async def send_inline_menu(chat_id):
    await bot.send_message(chat_id, '🍣', reply_markup=second_menu)
    inline_menu = get_inline_menu()
    await bot.send_message(chat_id, "Выберите на каких сайтах искать:", reply_markup=inline_menu)



