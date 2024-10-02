import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from loguru import logger

from database.models import User
from keyboards import menu_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """
    Старт бота, записывает в бд id пользователя если его ещё там нет.
    """
    User.get_or_create(tg_id=message.from_user.id, name=message.from_user.username)
    await message.answer('Этот бот поможет контроллировать нежелательные расходы, выберите действие',
                         reply_markup=await menu_keyboard())


@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    """
    Возвращение в главное меню.
    """
    await callback.message.answer('Главное меню', reply_markup=await menu_keyboard())
    await callback.answer()
