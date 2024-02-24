from datetime import datetime as dt
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from random import randrange

from loader import db, dp, bot
from states.acceptance_audio import AcceptanceAudioState


async def generate_audio_code():
    return randrange(100000, 999999)


@dp.message_handler(text_contains='/audio')
async def bot_echo(message: types.Message, state: FSMContext):
    audio_code = message.text.split(' ')[1]

    if not audio_code.isdigit():
        await message.answer(text="📝 Iltimos audio kodini tekshirib qayta urinib ko'ring.")
        return

    await state.update_data(audio_code=audio_code)
    await message.answer(text="🗣️ Audio faylni jo'nating:")
    await AcceptanceAudioState.audio.set()


@dp.message_handler(state=AcceptanceAudioState.audio, content_types=ContentTypes.ANY)
async def acceptance_audio(message: types.Message, state: FSMContext):
    if not message.content_type in ('audio', 'voice'):
        await message.answer(text="⚡ Iltimos ovozli habar ko'rinishida ovoz jo'nating.")
        await AcceptanceAudioState.audio.set()
        return

    if message.content_type == 'voice':
        audio = message.voice
    elif message.content_type == 'audio':
        audio = message.audio

    file_id = audio.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    audio_data = await state.get_data()
    audio_code = int(audio_data.get("audio_code"))
    telegram_id = str(message.from_user.id)

    await bot.download_file(file_path, f'../web/media/audios/{audio_code}.ogg')

    user_data = await db.select_user(telegram_id=telegram_id)
    user_id = int(user_data.get("id"))

    created_at = dt.now()

    await db.add_attempt(audio=f"audios/{audio_code}.ogg",
                         created_at=created_at,
                         user_id=user_id,
                         audio_code=audio_code
                         )
    await message.answer(text="✅ Audio fayl qabul qilindi.\n\nSaytga qaytib \"Boshlash\" tugmasini bosing.")
    await state.finish()
