from aiogram.dispatcher.filters.state import State, StatesGroup


class ResgisterState(StatesGroup):
    phone_number = State()
