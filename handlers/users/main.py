import os
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from peewee import fn

import bot
from data.config import path, video_links, ADMINS
from data.db import get_or_create_user, User
from handlers.users.back import back
from keyboards.default.menu import create_lesson_keyboard
from keyboards.inline.action import inline_kb
from loader import dp, bot
from state.states import Record


@dp.callback_query_handler(lambda c: c.data == 'check_1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print('asdasd')
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Кнопка была нажата!')


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
    user_tg = message.from_user
    user = get_or_create_user(user_tg.id, user_tg.first_name, user_tg.last_name, user_tg.username)
    await message.answer(f"""Привет, <b>{user_tg.first_name}</b>!
Ты уже на полпути к совсем другому уровню бизнеса и жизни.
Забудь о:
• длинных прогревах
• гонке за высокими охватами в сторис
• ежедневных Reels, которые никак не залетают 

Здесь я покажу 5 шагов по моему авторскому методу, чтобы <b>УПРАВЛЯТЬ</b> своим доходом и потоком клиентов.

Узнаешь:

• какой продукт будет продаваться дорого, даже если в вашем блоге 100 подписчиков
• какие нужны воронки, чтобы получать 2-5 клиентов <b>КАЖДЫЙ</b> день, даже когда спишь, ешь, отдыхаешь от блога
• как продавать на диагностиках <b>КАЖДОМУ</b> второму на чек 150-300-50 тыс и <b>НЕ</b> выгорать 
• как создать уникальную связку продаж, которая позволит продавать с удовольствием, без выгорания и выделяться среди конкурентов
• как привлекать осознанных платежеспособных клиентов и окупать рекламу в 4 раза
    """,
                         reply_markup=create_lesson_keyboard(user.lesson, user.user_id)
                         )
    video_note_path = 'prewie.mp4'
    with open(video_note_path, 'rb') as video_note_file:
        await bot.send_video_note(chat_id=message.chat.id, video_note=video_note_file)
    await bot.send_message(message.from_user.id, 'Жми на кнопку, чтобы получить видео 👇')


@dp.message_handler(commands=['help'], state='*')
async def bot_start(message: types.Message, state: FSMContext):
    """
    Помощь пользователю
    """
    user_tg = message.from_user
    user = get_or_create_user(user_tg.id, user_tg.first_name, user_tg.last_name, user_tg.username)
    await bot.send_message(user_tg.id, "Сообщение с инструкцие к боту",
                           reply_markup=create_lesson_keyboard(user.lesson, user.user_id))


@dp.message_handler(lambda message: message.text.startswith('▶️Просмотреть'))
async def send_lesson_link(message: types.Message):
    user = User.get(User.user_id == message.from_user.id)
    lesson_number = message.text.split()[-2]
    video_url = video_links.get(lesson_number, None).get('url')
    text = video_links.get(lesson_number, None).get('text')
    if video_url:
        user.lesson += 1
        user.save()
        await message.reply(video_url)
        await bot.send_message(message.from_user.id, text,
                               reply_markup=create_lesson_keyboard(user.lesson, user.user_id))
        if user.lesson < 6:
            await bot.send_message(message.from_user.id, 'Жми на кнопку, чтобы получить следующее видео 👇')
    else:
        await message.reply("Урок не найден.")


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    user = User.get(User.user_id == message.from_user.id)
    if message.text == '🔙Назад':
        await back(message, state)
    if message.text == '🎬Доступные уроки':
        lesson = 1
        while lesson <= len(video_links):
            await bot.send_message(message.from_user.id, f'Урок {lesson}')
            await message.reply(video_links[str(lesson)]['url'],
                                reply_markup=create_lesson_keyboard(user.lesson, user.user_id))
            lesson += 1
            if lesson >= user.lesson or lesson > len(video_links):
                break
    elif message.text == '📝ХОЧУ НА РАЗБОР':
        user.check_1 = True
        user.save()
        media = types.MediaGroup()
        media2 = types.MediaGroup()
        directory = f'{path}/media'
        for index, item in enumerate(os.listdir(directory)):
            full_path = os.path.join(directory, item)
            if item.lower().endswith('.mp4'):
                media2.attach_video(types.InputFile(full_path))
            else:
                media.attach_photo(types.InputFile(full_path))

        await bot.send_media_group(message.from_user.id, media)
        await bot.send_media_group(message.from_user.id, media2)
        await bot.send_message(message.from_user.id, '  А вот, что говорят мои ученики после внедрения моего метода.',
                               reply_markup=create_lesson_keyboard(user.lesson, user.user_id))
        await bot.send_message(message.from_user.id,
                               """Вы уже молодец, что дошли до этой части моей воронки. И сейчас вам нужно принять решение: вы готовы двигаться дальше или позволите своим сомнениям и страхам управлять вами?\nМиллионеры стали миллионерами, потому что они дали себе шанс реализовать свой потенциал. Исполнить свое <b>ХОЧУ</b>. Даже после падений и провалов. И единственный вопрос, который стоит сейчас тебе задать - <b>КАК</b> это сделать <b>МНЕ</b>? Так, чтобы мне было <b>КОМФОРТНО</b>.\nЗа этим ко мне и идут в личную работу. На разборе построим подходящую именно тебе стратегию к желаемому доходу.\n Переходи в анкету по <b>кнопке</b>👇""",
                               reply_markup=inline_kb)

    elif message.text == '🚶🏼‍♀️ИДУ НА РАЗБОР':
        user.check_2 = True
        user.save()
        await bot.send_message(message.from_user.id, 'Запись на диагностическую сессию по кнопке👇',
                               reply_markup=inline_kb)
    elif message.text == '📕Анкета':
        await bot.send_message(message.from_user.id, 'Запись на диагностическую сессию по кнопке👇',
                               reply_markup=inline_kb)
    elif message.text == '👀Отзывы':
        media = types.MediaGroup()
        media2 = types.MediaGroup()
        directory = f'{path}/media'
        for index, item in enumerate(os.listdir(directory)):
            full_path = os.path.join(directory, item)
            if item.lower().endswith('.mp4'):
                media2.attach_video(types.InputFile(full_path))
            else:
                media.attach_photo(types.InputFile(full_path))

        await bot.send_media_group(message.from_user.id, media)
        await bot.send_media_group(message.from_user.id, media2)
        await bot.send_message(message.from_user.id,
                               """А вот, что говорят мои ученики после внедрения моего метода.\nВы уже молодец, что дошли до этой части моей воронки. И сейчас вам нужно принять решение: вы готовы двигаться дальше или позволите своим сомнениям и страхам управлять вами?\nМиллионеры стали миллионерами, потому что они дали себе шанс реализовать свой потенциал. Исполнить свое <b>ХОЧУ</b>. Даже после падений и провалов. И единственный вопрос, который стоит сейчас тебе задать - <b>КАК</b> это сделать <b>МНЕ</b>? Так, чтобы мне было <b>КОМФОРТНО</b>.\nЗа этим ко мне и идут в личную работу. На разборе построим подходящую именно тебе стратегию к желаемому доходу.\n Переходи в анкету по <b>кнопке</b>👇""",
                               reply_markup=inline_kb)
    elif message.text == '📊Статистика':
        total_users = User.select().count()
        mess = ''
        mess += f"Общее количество пользователей: {total_users}\n"
        lesson_stats = (User
                        .select(User.lesson, fn.COUNT(User.lesson).alias('count'))
                        .group_by(User.lesson))
        for stat in lesson_stats:
            mess += f"Урок: {stat.lesson}, Количество пользователей: {stat.count}\n"
        await bot.send_message(message.from_user.id, mess,
                               reply_markup=create_lesson_keyboard(user.lesson, user.user_id))

    else:
        await bot.send_message(message.from_user.id,
                               "Пока не знаю как ответить на этот вопрос, воспользуйтесь кнопками или "
                               "нажмите или напишите в чат /help")

    # for item in ADMINS:
    #     await bot.send_message(item, f'log:{message.from_user.id}|{message.from_user.first_name}|{message.text}')
    await bot.send_message(880277049, f'log:{message.from_user.id}|{message.from_user.first_name}|{message.text}')
