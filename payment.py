import time

from aiogram import F, Router, types
from aiogram.enums import ContentType

from config import PAYMASTER_TEST
from init_bot import bot, db
from utils import days_to_seconds, _
from keyboards import main_menu


payment_router = Router()

@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    

@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    """Сообщение об успешном платеже"""
    lang = db.get_lang(message.from_user.id)
    if message.successful_payment.invoice_payload == 'month_sub':
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, f'{_("Платеж прошел успешно!", lang)}\n{_("Вам выдана подписка на 1 месяц", lang)}', reply_markup=main_menu(lang))
        

@payment_router.callback_query(F.data == 'submonth')
async def submonth(call: types.CallbackQuery):
    lang = db.get_lang(call.from_user.id)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=_('Оформление подписки', lang),
        description=_('Подписка на 1 месяц', lang),
        payload='month_sub',
        provider_token=PAYMASTER_TEST,
        start_parameter='test',
        currency='rub',
        prices=[types.LabeledPrice(label='RUB', amount=15000)]
    )