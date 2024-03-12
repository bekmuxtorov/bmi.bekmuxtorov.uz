from aiogram.dispatcher.filters.state import State, StatesGroup


class AcceptanceAudioState(StatesGroup):
    audio = State()
