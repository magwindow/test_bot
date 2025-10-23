from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# main menu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❤️ Подписаться'),
            KeyboardButton(text='👤 Мой профиль'),
        ],
        [
            KeyboardButton(text='👥 Список пользователей')
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

# subscribe inline channel
sub_channel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подписаться', url='https://t.me/test_channel_test_test24'),
            InlineKeyboardButton(text='✅ Уже подписан', callback_data='subchannel')
        ]
    ]
)


