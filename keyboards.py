from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



# main menu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❤️ Подписаться'),
            KeyboardButton(text='👤 Мой профиль'),
        ],
        [
            KeyboardButton(text='👥 Список пользователей'),
            KeyboardButton(text='👀 Другое')
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

# other inline buttons
other_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👉 Перейти на канал', url='https://t.me/test_channel_test_test24'),
            InlineKeyboardButton(text='📢 Поделиться с друзьями', switch_inline_query='Лучший бот в мире!'),
        ],
        [
            InlineKeyboardButton(text='🔶 Рандомное число', callback_data='btn_random'),
            InlineKeyboardButton(text='Что-то', switch_inline_query_current_chat='Тест'),
        ],
    ]
)


crypto_list_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Bitcoin', callback_data='cc_bitcoin'),
            InlineKeyboardButton(text='Ethereum', callback_data='cc_ethereum'),
            InlineKeyboardButton(text='Solana', callback_data='cc_solana'),
        ],
    ]
)


