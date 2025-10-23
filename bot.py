import asyncio
import logging

from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ContentType

from config import TOKEN, PAYMASTER_TEST
from keyboards import main_menu, sub_inline_markup

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Привет, {0.first_name}!'.format(message.from_user), reply_markup=main_menu)
    


@dp.message(F.text == '❤️ Подписаться')
async def bot_message(message: types.Message):
    print(message.chat.type)
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Выберите подписку', reply_markup=sub_inline_markup)


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
    
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    

@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    await bot.send_message(message.from_user.id, 'Платеж прошел успешно')
    
    
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())