import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.default_buttons import contact_request_button
from states.register import ResgisterState
from random import randrange


async def generate_confirmed_code():
    return randrange(100000, 999999)


async def writing_code_message(confirm_code: int) -> str:
    return f"🔐 Kodingiz: <mono>{confirm_code}</mono>"


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if not user:
        await message.answer(text="Salom Pavel 👋/nhttps://soundtotext.bekmuxtorov.uz'ning rasmiy botiga xush kelibsiz!\n\n⬇️ Kontaktingizni yuboring(tugmani bosib)", reply_markub=contact_request_button)
        await ResgisterState.phone_number.set()
    else:
        text = "🔑 Yangi kod olish uchun /login ni bosing"
        await message.answer(text=text)


@dp.message_handler(state=ResgisterState.phone_number, content_types="contact")
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    try:
        confirm_code = await generate_confirmed_code()
        await db.add_user(
            phone_number=phone_number,
            telegram_id=telegram_id,
            full_name=full_name,
            confirm_code=confirm_code
        )
        text = await writing_code_message(confirm_code)
        await message.answer(text=text)
        await state.finish()

    except Exception as e:
        print(e)


@dp.message_handler(text="/login")
async def set_password(message: types.Message):
    user_id = message.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if user:
        confirm_code = await generate_confirmed_code()
        await db.update_user_confirm_code(
            confirm_code=confirm_code,
            telegram_id=message.from_user.id
        )
        text = await writing_code_message(confirm_code)
        await message.answer(text=text)
    else:
        await message.answer(text="Salom Pavel 👋/nhttps://soundtotext.bekmuxtorov.uz'ning rasmiy botiga xush kelibsiz!\n\n⬇️ Kontaktingizni yuboring(tugmani bosib)", reply_markub=contact_request_button)
        await ResgisterState.phone_number.set()
