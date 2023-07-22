import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from loguru import logger
import bot
from data.config import ADMINS, path
from handlers.users.back import back
from keyboards.default.menu import menu_admin, second_menu, menu
from keyboards.inline.action import button_states, update_button_icon, send_inline_menu, price, nums
from loader import dp, bot

# Словарь для хранения состояний кнопок
from parsers.East import east
from parsers.Empire import empire
from parsers.House import house
from parsers.Make import make
from state.states import Sushi


# Колбэк-обработчик для инлайн-кнопок
@dp.callback_query_handler(lambda c: True, state=[Sushi.choice_shops])
async def inline_callback_handler(callback_query: types.CallbackQuery, state):
    async with state.proxy() as dataq:
        data = callback_query.data
        # Обработка нажатия на кнопку и изменение иконки
        if data in button_states:
            button_states[data] = not button_states[data]
            await update_button_icon(callback_query.message, data)
        if data == 'ok':
            dataq['shops'] = button_states
            result = any(value for value in button_states.values())
            if result:
                await Sushi.choice_price.set()
                await bot.send_message(callback_query.from_user.id, 'Выберите диапозон цены:', reply_markup=price)
            else:
                await bot.send_message(callback_query.from_user.id, 'Не выбран сайт')
                await send_inline_menu(chat_id=callback_query.from_user.id)


@dp.callback_query_handler(lambda c: True, state=[Sushi.choice_price])
async def inline_callback_handler(callback_query: types.CallbackQuery, state):
    async with state.proxy() as dataq:
        data = callback_query.data
        dataq['price'] = data
        await Sushi.choice_nums.set()
        await bot.send_message(callback_query.from_user.id, 'Сколько показать вариантов?', reply_markup=nums)


@dp.callback_query_handler(lambda c: True, state=[Sushi.choice_nums])
async def inline_callback_handler(callback_query: types.CallbackQuery, state):
    async with state.proxy() as dataq:
        list_sets = []
        data = callback_query.data
        dataq['nums'] = data
        shops = dataq.get('shops')
        price = int(dataq.get('price'))
        nums = int(dataq.get('nums'))
        if shops['button1']:
            await bot.send_message(callback_query.from_user.id, 'Сканируется Суши Восток')
            list_sets.extend(east())
        if shops['button2']:
            await bot.send_message(callback_query.from_user.id, 'Сканируется Империя')
            list_sets.extend(empire())
        if shops['button3']:
            await bot.send_message(callback_query.from_user.id, 'Сканируется Японский домик')
            list_sets.extend(house())
        if shops['button4']:
            await bot.send_message(callback_query.from_user.id, 'Сканируется Суши-make')
            list_sets.extend(make())

        sorted_sushi_sets = sorted(list_sets, key=lambda x: x.coefficient, reverse=False)
        for i in sorted_sushi_sets:
            if nums == 0:
                break
            if price == 500:
                if 0 < i.price <= 500:
                    if i.image:
                        photo = types.InputFile.from_url(i.image)
                        await bot.send_photo(callback_query.from_user.id, photo)
                    await bot.send_message(callback_query.from_user.id,
                                           f'Наименование: {i.name}\n💰Цена: {i.price} руб.\n'
                                           f'⚖Вес: {i.weight} гр.\n🪙Цена за грамм: {i.coefficient} руб.'
                                           f'\n🔗Ссылка: {i.url}', disable_web_page_preview=True, parse_mode='HTML'
                                           )
                    nums -= 1
            elif price == 1000:
                if 501 < i.price <= 1000:
                    if i.image:
                        photo = types.InputFile.from_url(i.image)
                        await bot.send_photo(callback_query.from_user.id, photo)
                    await bot.send_message(callback_query.from_user.id,
                                           f'Наименование: {i.name}\n💰Цена: {i.price} руб.\n'
                                           f'⚖Вес: {i.weight} гр.\n🪙Цена за грамм: {i.coefficient} руб.'
                                           f'\n🔗Ссылка: {i.url}', disable_web_page_preview=True, parse_mode='HTML'
                                           )
                    nums -= 1
            elif price == 1500:
                if 1001 < i.price <= 1500:
                    if i.image:
                        photo = types.InputFile.from_url(i.image)
                        await bot.send_photo(callback_query.from_user.id, photo)
                    await bot.send_message(callback_query.from_user.id,
                                           f'Наименование: {i.name}\n💰Цена: {i.price} руб.\n'
                                           f'⚖Вес: {i.weight} гр.\n🪙Цена за грамм: {i.coefficient} руб.'
                                           f'\n🔗Ссылка: {i.url}', disable_web_page_preview=True, parse_mode='HTML'
                                           )
                    nums -= 1
            elif price == 2000:
                if 1501 < i.price:
                    if i.image:
                        photo = types.InputFile.from_url(i.image)
                        await bot.send_photo(callback_query.from_user.id, photo)
                    await bot.send_message(callback_query.from_user.id,
                                           f'Наименование: {i.name}\n💰Цена: {i.price} руб.\n'
                                           f'⚖Вес: {i.weight} гр.\n🪙Цена за грамм: {i.coefficient} руб.'
                                           f'\n🔗Ссылка: {i.url}', disable_web_page_preview=True, parse_mode='HTML'
                                           )
                    nums -= 1
            elif price == 0:
                if i.image:
                    photo = types.InputFile.from_url(i.image)
                    await bot.send_photo(callback_query.from_user.id, photo)
                await bot.send_message(callback_query.from_user.id,
                                       f'Наименование: {i.name}\n💰Цена: {i.price} руб.\n'
                                       f'⚖Вес: {i.weight} гр.\n🪙Цена за грамм: {i.coefficient} руб.'
                                       f'\n🔗Ссылка: {i.url}', disable_web_page_preview=True, parse_mode='HTML'
                                       )
                nums -= 1


@dp.message_handler(commands=['start'], state='*')
async def bot_start(message: types.Message, state: FSMContext):
    """
    Старт бота, проверка на присутствие в базе данных, если нет, запрашивает пароль
    """
    logger.info('Пользователь {}: {} {} нажал на кнопку {}'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.text
    ))
    hello = ['limur.tgs', 'Dicaprio.tgs', 'hello.tgs', 'hello2.tgs', 'hello3.tgs']
    sticker = open('{}/stikers/{}'.format(path, random.choice(hello)), 'rb')
    await bot.send_sticker(message.chat.id, sticker)
    await message.answer('Добро пожаловать, {}!'
                         '\nБот для показа выгодных предложений ролл сетов'
                         .format(message.from_user.first_name),
                         reply_markup=menu)


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, message.text)
    if message.text == 'Назад':
        await back(message, state)
    if message.text == 'Найти сеты':
        await send_inline_menu(chat_id=message.from_user.id)
        await Sushi.choice_shops.set()
