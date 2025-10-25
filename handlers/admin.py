from aiogram import Router, types
from aiogram.filters import Command

from config import ADMIN_ID
from keyboards import main_menu
from init_bot import bot, db
from utils import _


admin_router = Router()

@admin_router.message(Command('sendall'))
async def send_all(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    """Администратор отправляет сообщение всем пользователям, командой /sendall <Сообщение>"""
    if message.chat.type == 'private':
        if message.from_user.id == ADMIN_ID:
            for row in db.get_users():
                try:
                    await bot.send_message(row[0], message.text[9:])
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
                    
            if message.text[9:] == '':
                await bot.send_message(message.from_user.id, _('Ваше сообщение должно содержать /sendall <Сообщение>', lang), reply_markup=main_menu(lang))
                return
            await bot.send_message(message.from_user.id, _('Сообщение отправлено всем пользователям', lang), reply_markup=main_menu(lang))