import os
import asyncio
from peewee import *

from aiogram import Bot, Dispatcher

from loguru import logger
from dotenv import load_dotenv, find_dotenv

from handlers.user_handlers import router
from database.models import create_new_tables
from handlers.states import state_router

load_dotenv(find_dotenv())

async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(state_router, router)
    await create_new_tables()
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        logger.info('START bot')
        asyncio.run(main())
    except:
        logger.error('ERROR run bot')
   
