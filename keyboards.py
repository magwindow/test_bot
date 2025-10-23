from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# main menu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❤️ Подписаться'),
            KeyboardButton(text='⚙️ Настройки')
        ]
    ],
    resize_keyboard=True
)

# subscribe inline buttons
sub_inline_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подписаться на 1 месяц', callback_data='submonth')
        ]
    ]
)


