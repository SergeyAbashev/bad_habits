from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def get_category_keyboard():
    """
    Клавиатура выбора категории для добавления расхода.
    """
    category_keyboard = [
        [InlineKeyboardButton(text='Пиво', callback_data='beer')],
        [InlineKeyboardButton(text='Сигареты', callback_data='cigarettes')],
        ]
    return InlineKeyboardMarkup(inline_keyboard=category_keyboard)


async def menu_keyboard():
    """
    Клавиатура выбора действия: Добавить или Показать расход.
    """
    menu_keyboard = [
        [InlineKeyboardButton(text='Добавить расход', callback_data='add_pyment')],
        [InlineKeyboardButton(text='Показать расходы', callback_data='show_pyments')],
        ]
    return InlineKeyboardMarkup(inline_keyboard=menu_keyboard)


async def show_payments_for_the_period():
    """
    Клавиатура выбора месяца.
    """
    show_period_keyboard = [
        [InlineKeyboardButton(text='Январь', callback_data='1')],
        [InlineKeyboardButton(text='Февраль', callback_data='2')],
        [InlineKeyboardButton(text='Март', callback_data='3')],
        [InlineKeyboardButton(text='Апрель', callback_data='4')],
        [InlineKeyboardButton(text='Февраль', callback_data='2')],
        [InlineKeyboardButton(text='Май', callback_data='5')],
        [InlineKeyboardButton(text='Июнь', callback_data='6')],
        [InlineKeyboardButton(text='Июль', callback_data='7')],
        [InlineKeyboardButton(text='Август', callback_data='8')],
        [InlineKeyboardButton(text='Сентябрь', callback_data='9')],
        [InlineKeyboardButton(text='Октябрь', callback_data='10')],
        [InlineKeyboardButton(text='Ноябрь', callback_data='11')],
        [InlineKeyboardButton(text='Декабрь', callback_data='12')],
        [InlineKeyboardButton(text='Меню', callback_data='back')],
        ]
    return InlineKeyboardMarkup(inline_keyboard=show_period_keyboard)