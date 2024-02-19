from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


contact_request_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="☎️ Kontaktni yuborish",
                request_contact=True
            )
        ],
    ]
)
