import asyncio
import logging
import time
import random
from pycoingecko import CoinGeckoAPI

from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.enums import ContentType

from config import ADMIN_ID, TOKEN, PAYMASTER_TEST, CHANNEL_ID
from keyboards import (main_menu, sub_inline_markup, sub_channel_markup, other_inline_menu, crypto_list_inline)
from database import Database
from utils import check_sub_channel, days_to_seconds, time_sub_day

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
cg = CoinGeckoAPI()
db = Database('users.db')


@dp.message(CommandStart())
async def start(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Укажите никнейм')
        else:
            if message.from_user.id == ADMIN_ID:
                await bot.send_message(message.from_user.id, 'Вы администратор. Введите /sendall <Сообщение> чтобы начать рассылку.', reply_markup=main_menu)
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы\n'
                                   'Чтобы узнать текущую стоимость криптовалюты, введите /crypto', reply_markup=main_menu)
    else:
        await bot.send_message(message.from_user.id, 'Вы не подписаны на канал', reply_markup=sub_channel_markup)
        

@dp.message(Command('sendall'))
async def send_all(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == ADMIN_ID:
            for row in db.get_users():
                try:
                    await bot.send_message(row[0], message.text[9:])
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(message.from_user.id, 'Сообщение отправлено всем пользователям', reply_markup=main_menu)
        
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    

@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_sub':
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, 'Платеж прошел успешно!\nВам выдана подписка на 1 месяц', reply_markup=main_menu)
    
@dp.message()
async def bot_message(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        if message.chat.type == 'private':
            
            # get crypto
            name_crypto = ''
            price_crypto = ''
            for key, value in cg.get_price(ids=message.text, vs_currencies='usd').items():
                name_crypto = key
                price_crypto = value['usd']
            
            
            if message.text == '❤️ Подписаться':
                await bot.send_message(message.from_user.id, 'Выберите подписку', reply_markup=sub_inline_markup)
            
            elif message.text == '👤 Мой профиль':
                user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
                if not user_sub:
                    await bot.send_message(message.from_user.id, f'Ваш никнейм: {db.get_nickname(message.from_user.id)}\n'
                                        f'Ваша подписка: неактивна', reply_markup=main_menu)
                else:
                    await bot.send_message(message.from_user.id, f'Ваш никнейм: {db.get_nickname(message.from_user.id)}\n'
                                        f'Ваша подписка: {user_sub}', reply_markup=main_menu)
            
            elif message.text == '👥 Список пользователей':
                if db.get_sub_status(message.from_user.id):
                    await bot.send_message(message.from_user.id, 'Список пользователей:', reply_markup=main_menu)
                else:
                    await bot.send_message(message.from_user.id, 'Сначала оформите подписку', reply_markup=main_menu)
                    
            elif message.text == '👀 Другое':
                await bot.send_message(message.from_user.id, 'Раздел другое:', reply_markup=other_inline_menu)
                
            elif message.text == '/crypto':
                await bot.send_message(message.from_user.id, 'Выберите криптовалюту или напишите в чат название, например, Cardano', reply_markup=crypto_list_inline)
            
            elif message.text.lower() == name_crypto:
                await bot.send_message(message.from_user.id, 
                                       f'Стоимость {message.text}: {price_crypto}$', reply_markup=crypto_list_inline)
            
            else:
                if db.get_signup(message.from_user.id) == 'setnickname':
                    if len(message.text) > 15:
                        await bot.send_message(message.from_user.id, 'Никнейм не должен превышать 15 символов')
                    elif '@' in message.text or '/' in message.text:
                        await bot.send_message(message.from_user.id, 'Никнейм не должен содержать @ или /')
                    else:
                        db.set_nickname(message.from_user.id, message.text)
                        db.set_signup(message.from_user.id, 'active')
                        await bot.send_message(message.from_user.id, 'Вы успешно зарегистрировались', reply_markup=main_menu)
                else:
                    await bot.send_message(message.from_user.id, 'Что-то пошло не так', reply_markup=main_menu)
    else:
        await bot.send_message(message.from_user.id, 'Вы не подписаны на канал', reply_markup=sub_channel_markup)
 
 
@dp.callback_query(F.data.startswith('cc_')) 
async def crypto(call: types.CallbackQuery):
    currency = call.data.split('_')[-1]
    result = cg.get_price(ids=currency, vs_currencies='usd')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, f'Стоимость {currency}: {result[currency]["usd"]}$', reply_markup=crypto_list_inline)               

@dp.callback_query(F.data == 'submonth')
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title='Оформление подписки',
        description='Подписка на 1 месяц',
        payload='month_sub',
        provider_token=PAYMASTER_TEST,
        start_parameter='test',
        currency='rub',
        prices=[types.LabeledPrice(label='RUB', amount=15000)]
    )
    
@dp.callback_query(F.data == 'subchannel')
async def subchannel(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
    
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Укажите никнейм')
        else:
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы', reply_markup=main_menu)
    else:
        await bot.send_message(message.from_user.id, 'Вы не подписаны на канал', reply_markup=sub_channel_markup)
        

@dp.callback_query(F.data == 'btn_random')
async def randomize(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
    await bot.send_message(message.from_user.id, f'Случайное число: {random.randint(1, 100)}', reply_markup=other_inline_menu)    

      
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())