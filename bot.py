import asyncio
import logging
import time
import datetime

from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ContentType

from config import TOKEN, PAYMASTER_TEST
from keyboards import main_menu, sub_inline_markup
from database import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

db = Database('users.db')


def days_to_seconds(days):
    return days * 86400


@dp.message(CommandStart())
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Укажите никнейм')
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы', reply_markup=main_menu)
        
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
    if message.chat.type == 'private':
        if message.text == '❤️ Подписаться':
            await bot.send_message(message.from_user.id, 'Выберите подписку', reply_markup=sub_inline_markup)
        elif message.text == '👤 Мой профиль':
            signup = db.get_signup(message.from_user.id)
            await bot.send_message(message.from_user.id, f'Ваш никнейм: {db.get_nickname(message.from_user.id)}\nВаша подписка: {signup}')
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
      
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())