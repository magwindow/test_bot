from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS
from utils import _


def main_menu(lang):
    """Главное меню"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('❤️ Подписаться', lang)),
                KeyboardButton(text=_('👤 Мой профиль', lang)),
            ],
            [
                KeyboardButton(text=_('👥 Список пользователей', lang)),
                KeyboardButton(text=_('👀 Другое', lang)),
            ]
        ],
        resize_keyboard=True
    )
    return kb


def sub_menu(lang):
    """Следующий раздел меню"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('💸 Курс USD/RUB', lang)),
                KeyboardButton(text=_('📝 Информация', lang)),
            ],
            [
                KeyboardButton(text=_('🔙 Назад', lang)),
                KeyboardButton(text=_('🌐 Сменить язык', lang)),
            ]
        ],
        resize_keyboard=True
    )
    return kb

def sub_inline_markup(lang):
    """Инлайн кнопки подписки"""
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('Подписаться на 1 месяц', lang), callback_data='submonth')
            ]
        ]
    )
    return kb


def other_inline_menu(lang):
    """Разные инлайн кнопки"""
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('👉 Перейти на канал', lang), url='https://t.me/test_channel_test_test24'),
                InlineKeyboardButton(text=_('📢 Поделиться с друзьями', lang), switch_inline_query='Лучший бот в мире!'),
            ],
            [
                InlineKeyboardButton(text=_('🔶 Рандомное число', lang), callback_data='btn_random'),
                InlineKeyboardButton(text=_('Что-то', lang), switch_inline_query_current_chat='Тест'),
            ],
        ]
    )
    return kb

def crypto_list_inline(lang):
    """Кнопки списка криптовалют"""
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('Bitcoin', lang), callback_data='cc_bitcoin'),
                InlineKeyboardButton(text=_('Ethereum', lang), callback_data='cc_ethereum'),
                InlineKeyboardButton(text=_('Solana', lang), callback_data='cc_solana'),
            ],
        ]
    )
    return kb


# subscribe inline channel
sub_channel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=CHANNELS[0][0], url=CHANNELS[0][2]),
            InlineKeyboardButton(text=CHANNELS[1][0], url=CHANNELS[1][2]),
            InlineKeyboardButton(text='✅ Уже подписан', callback_data='subchannel')
        ]
    ]
)

# language inline buttons
lang_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru'),
            InlineKeyboardButton(text='🇬🇧 English', callback_data='lang_en'),
        ]
    ]
)








