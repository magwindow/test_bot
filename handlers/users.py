import random
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command

from pycoingecko import CoinGeckoAPI

from utils import _
from bad_words import BAD_WORDS
from config import ADMIN_ID, BOT_NICKNAME, CHANNELS
from utils import check_sub_channels, get_rate, recognize_question, time_sub_day
from init_bot import bot, db
from keyboards import (main_menu, sub_channel_markup, sub_inline_markup, other_inline_menu, 
                       crypto_list_inline, sub_menu, lang_menu)

user_router = Router()

@user_router.message(CommandStart())
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
    # Регистрация пользователя через реферальную ссылку
        referrer_id = message.text[7:]
        if str(referrer_id).isdigit() and str(referrer_id) != str(message.from_user.id):
            db.add_user(message.from_user.id, referrer_id)
            lang = db.get_lang(message.from_user.id)           
            try:
                await bot.send_message(referrer_id, f'{_("Ваш реферал", lang)} {message.from_user.id} {_("зарегистрировался", lang)}')
            except:
                pass  
        else:
            await bot.send_message(message.from_user.id, _('Вы не подписаны на канал'), reply_markup=sub_channel_markup)
        
    else:    
        # Сообщения всем зарегестрированным пользователям
        lang = db.get_lang(message.from_user.id)
        await bot.send_message(message.from_user.id, f'{_("Вы уже зарегистрированы", lang)}\n'
                              f'{_("Чтобы узнать текущую стоимость криптовалюты, введите /crypto", lang)}', reply_markup=main_menu(lang))
    
    
    
    # Если пользователь является администратором
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(message.from_user.id, _('Вы администратор. Введите /sendall <Сообщение> чтобы начать рассылку.', lang), reply_markup=main_menu(lang))
                    
    
    
 

@user_router.message(Command('crypto'))
async def user_command_crypto(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, _('Выберите криптовалюту:', lang), reply_markup=crypto_list_inline(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)        


@user_router.message(F.text.in_(['❤️ Подписаться', '❤️ Subscribe']))
async def user_subscribe(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, _('Выберите подписку', lang), reply_markup=sub_inline_markup(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)
        

@user_router.message(F.text.in_(['👤 Мой профиль', '👤 My profile']))
async def user_profile(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if not user_sub:
                await bot.send_message(message.from_user.id, f'{_("Ваш никнейм:", lang)} {db.get_nickname(message.from_user.id)}\n'
                                    f'{_("Ваша подписка: неактивна", lang)}\n\n{_("Реферальная ссылка", lang)}\nhttps://t.me/{BOT_NICKNAME}?start={message.from_user.id}\n'
                                    f'{_("Количество рефералов:", lang)} {db.count_referals(message.from_user.id)}', reply_markup=main_menu(lang))
            else:
                user_sub = user_sub.split()
                await bot.send_message(message.from_user.id, f'{_("Ваш никнейм:", lang)} {db.get_nickname(message.from_user.id)}\n'
                                    f'{_("Ваша подписка:", lang)} {user_sub[0]} {_(user_sub[1], lang)} {user_sub[-1]}\n\n\n{_("Реферальная ссылка", lang)}\nhttps://t.me/{BOT_NICKNAME}?start={message.from_user.id}\n'
                                    f'{_("Количество рефералов:", lang)} {db.count_referals(message.from_user.id)}', reply_markup=main_menu(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)


@user_router.message(F.text.in_(['👥 Список пользователей', '👥 List of users']))
async def user_list(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            if db.get_sub_status(message.from_user.id):
                await bot.send_message(message.from_user.id, _('Список пользователей:', lang), reply_markup=main_menu(lang))
            else:
                await bot.send_message(message.from_user.id, _('Сначала оформите подписку', lang), reply_markup=main_menu(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)
        

@user_router.message(F.text.in_(['👀 Другое', '👀 Other']))
async def user_other(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, _('Раздел другое:', lang), reply_markup=sub_menu(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)
        

@user_router.message(F.text.in_(['🔙 Назад', '🔙 Back']))
async def back_to_main_menu(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, _('Вы вернулись в главное меню', lang), reply_markup=main_menu(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)
        

@user_router.message(F.text.in_(['📝 Информация', '📝 Information']))
async def back_to_main_menu(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, _('Информация:', lang), reply_markup=other_inline_menu(lang))
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)
        
@user_router.message(F.text.in_(['💸 Курс USD/RUB', '💸 Rate USD/RUB']))
async def get_usd_rub(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    if await check_sub_channels(CHANNELS, message.from_user.id):
        if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, f'{_("Текущий курс:", lang)} {get_rate()} {_("руб.", lang)}')
    else:
        await bot.send_message(message.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)
        
@user_router.message(F.text.in_(['🌐 Сменить язык', '🌐 Change language']))
async def change_language(message: types.Message):
    await bot.send_message(message.from_user.id, _('Выбери язык:'), reply_markup=lang_menu)
        

@user_router.message(F.text)
async def set_nickname(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    # Проверяем, действительно ли мы ждём ник
    if db.get_signup(message.from_user.id) == 'setnickname':
        nickname = message.text.strip()

        if len(nickname) > 15:
            await bot.send_message(message.from_user.id, _('Никнейм не должен превышать 15 символов', lang))
        elif '@' in nickname or '/' in nickname:
            await bot.send_message(message.from_user.id, _('Никнейм не должен содержать @ или /', lang))
        else:
            db.set_nickname(message.from_user.id, nickname)
            db.set_signup(message.from_user.id, 'active')
            await bot.send_message(message.from_user.id, _('Ваш никнейм обновлен ✅', lang), reply_markup=main_menu(lang))
    # filter bad words
    elif message.text in BAD_WORDS:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot.send_message(message.from_user.id, _('Недопустимое сообщение', lang), reply_markup=main_menu(lang))
    else:
        # Ответ бота на вопросы
        answer_id = recognize_question(message.text, db.get_question())
        await bot.send_message(message.from_user.id, db.get_answer(answer_id), reply_markup=main_menu(lang))
        

@user_router.callback_query(F.data.startswith('cc_')) 
async def crypto(call: types.CallbackQuery):
    """Показывает стоимость выбранной криптовалюты"""
    lang = db.get_lang(call.from_user.id)
    cg = CoinGeckoAPI()
    currency = call.data.split('_')[-1]
    result = cg.get_price(ids=currency, vs_currencies='usd')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, f'{_("Стоимость", lang)} {currency}: {result[currency]["usd"]}$', reply_markup=crypto_list_inline(lang)) 
    
    
@user_router.callback_query(F.data.startswith('lang_'))
async def set_language(call: types.CallbackQuery):
    db.change_lang(call.from_user.id, call.data.split('_')[-1])
    lang = db.get_lang(call.from_user.id)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    if await check_sub_channels(CHANNELS, call.from_user.id):
        if not db.user_exists(call.from_user.id):
            lang = call.data.split('_')[-1]
            db.set_signup(call.from_user.id, 'setnickname')
        elif db.get_signup(call.from_user.id) != 'active':
            await bot.send_message(call.from_user.id, f'{_("Отлично, теперь напиши свой никнейм", lang)}\n{_("(до 15 символов, без @ и /)", lang)}')
        else:
            await bot.send_message(call.from_user.id, _('Вы сменили язык', lang), reply_markup=main_menu(lang)) 
    
    else:
        await bot.send_message(call.from_user.id, _('Вы не подписаны на канал', lang), reply_markup=sub_channel_markup)            


@user_router.callback_query(F.data == 'subchannel')
async def subchannel(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    
    if await check_sub_channels(CHANNELS, call.from_user.id):
        if not db.user_exists(call.from_user.id):
            db.add_user(call.from_user.id)
            await bot.send_message(call.from_user.id, _('Выбери язык:'), reply_markup=lang_menu)
        else:
            await bot.send_message(call.from_user.id, _('Вы уже зарегистрированы'))
    else:
        await bot.send_message(call.from_user.id, _('Вы не подписаны на канал'), reply_markup=sub_channel_markup)
        
                

@user_router.callback_query(F.data == 'btn_random')
async def randomize(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
    await bot.send_message(message.from_user.id, f'{_("Случайное число:", lang)} {random.randint(1, 100)}', reply_markup=other_inline_menu(lang))