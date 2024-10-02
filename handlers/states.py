import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from loguru import logger

from database.models import Pyment
from keyboards import get_category_keyboard, menu_keyboard, show_payments_for_the_period

state_router = Router()


class Amount(StatesGroup):
    category = State()  #'beer' или 'cigarettes'
    pyment = State()    # Сумма.


class Show_pyment(StatesGroup):
    period = State()


@state_router.callback_query(F.data == 'show_pyments')
async def show_pyments(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Show_pyment.period)
    await callback.message.answer('Выберите период', 
                                reply_markup=await show_payments_for_the_period())


@state_router.callback_query(Show_pyment.period)
async def process_period(callback: CallbackQuery, state: FSMContext):
    await state.update_data(period=callback.data)
    data = await state.get_data()
    month_dict = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель',
                  '5': 'Май', '6': 'Июнь', '7': 'Июль', '8': 'Август',
                  '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}
    select_month = Pyment.select().where(Pyment.user_id == callback.from_user.id and 
                                         Pyment.pyment_data.month == int(data['period']))
    if select_month:
        for _ in select_month:
            summ_beer = sum(result.beer for result in select_month)
            summ_cigarettes = sum(result.cigarettes for result in select_month)
        await callback.message.answer(f'Расходы за {month_dict[data["period"]]}:\n'
                                    f'Сумма расходов на пиво: {summ_beer}\n'
                                    f'Сумма расходов на сигареты: {summ_cigarettes}', 
                                    reply_markup=await menu_keyboard())
    else:
        await callback.message.answer('Нет расходов')
   
    await state.clear()
    

@state_router.callback_query(F.data == 'beer')
async def process_beer(callback: CallbackQuery, state: FSMContext):
    """
    На событие 'beer' записываем в состояние пиво,
    в ожидание сумма.
    """
    await state.update_data(category='beer')
    await state.set_state(Amount.pyment)
    await callback.message.answer('Введите сумму')
    await callback.answer()


@state_router.callback_query(F.data == 'cigarettes')
async def process_cigarettes(callback: CallbackQuery, state: FSMContext):
    """
    На событие 'cigarettes' записываем в состояние сигареты,
    в ожидание сумма.
    """
    await state.update_data(category='cigarettes')
    await state.set_state(Amount.pyment)
    await callback.message.answer('Введите сумму')
    await callback.answer()


@state_router.message(Amount.pyment)
async def process_pyment(message: Message, state: FSMContext):
    """
    На событие сумма записываем в состояние сумма,
    сохраняем словарь состояние: значение,
    запись в бд полученных значений, в зависимости от категории.
    """
    if message.text.isdigit():
        await state.update_data(pyment=message.text)
        logger.info('process_pyment')
    else:
        await message.answer('Введите число')
        logger.info('process_pyment not digit')
        
    data = await state.get_data()

    category_dict = {'beer': 'Пиво', 'cigarettes': 'Сигареты'}

    if data['category'] == 'beer':
        Pyment(beer=data['pyment'],
                cigarettes=0,
                pyment_data=datetime.date.today(),
                user_id=message.from_user.id).save()
    else:
        Pyment(beer=0,
                cigarettes=data['pyment'],
                pyment_data=datetime.date.today(),
                user_id=message.from_user.id).save()
    await message.answer(f"Данные записаны: \n"
                         f"Потрачено {data['pyment']} на {category_dict[data['category']]}", 
                         reply_markup=await menu_keyboard())
    await state.clear()


@state_router.callback_query(F.data == 'add_pyment')
async def repeat_amount(callback: CallbackQuery, state: FSMContext):
    """
    На событие "Добавить платёж" после выполненого сценария,
    запускаем снова сценарий.
    """
    await state.set_state(Amount.category)
    await callback.message.answer('Выберите категорию', 
                                  reply_markup=await get_category_keyboard())
