from aiogram.dispatcher.filters.state import StatesGroup, State


class Sushi(StatesGroup):
    choice_shops = State()
    choice_price = State()
    choice_nums = State()


