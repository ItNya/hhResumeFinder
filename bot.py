from HHru import *
import json
from os import path
from pathlib import Path
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext


import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='')

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup): # ячейка в которой сохроняются ответы пользователя:
    city = State()
    pof = State()
    experience = State()
    gender = State()
    zp_ot = State()
    zp_do = State()


@dp.message_handler(commands="help")
async def cmd_test1(message: types.Message):
    await message.answer('--СПРАВКА ДЛЯ ПОЛЬЗОВАТЕЛЯ--\n'
                         '|для того чтобы начать поиск введите команду /start|'
                         '\nДалее вам будет предложено ввести местность, професию , опыт работы и пол сотрудника\
                         nПосле ввода данных начнётся поиск.\n'
                         'PS:Приятного пользования\n'
                         'Так как данный поисковой бот создан не проффесионалами возможны ошибки.')


@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await message.answer('Введите город/регион/область/страну поиска:')

    await Form.city.set()


@dp.message_handler(state=Form.city)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)


    await message.answer('Введите нужную вам профессию:')

    await Form.next()

@dp.message_handler(state=Form.pof)
async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")

    answer2 = message.text

    await state.update_data(answer2=answer2)

    await message.answer('Введите желаемый опыт работы сотрудника(Пример: 0, 3, 6, 10):')

    await Form.next()

@dp.message_handler(state=Form.experience)
async def answer_q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")

    answer2 = data.get("answer2")

    answer3 = message.text

    await state.update_data(answer3=answer3)

    await message.answer('Введите желаемый пол сотрудника(Пример: Женский, Мужской, Не важен):')

    await Form.next()

@dp.message_handler(state=Form.gender)
async def answer_q4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")

    answer2 = data.get("answer2")

    answer3 = data.get("answer3")

    answer4 = message.text

    await state.update_data(answer4=answer4)

    await message.answer('Введите начальную заработную плату(Пример: 50000):')

    await Form.next()


@dp.message_handler(state=Form.zp_ot)
async def answer_q5(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")

    answer2 = data.get("answer2")

    answer3 = data.get("answer3")

    answer4 = data.get("answer4")

    answer5 = message.text

    await state.update_data(answer5=answer5)

    await message.answer('Введите конечную заработную плату(Пример: 300000):')

    await Form.next()


@dp.message_handler(state=Form.zp_do)
async def answer_q5(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")

    answer2 = data.get("answer2")

    answer3 = data.get("answer3")

    answer4 = data.get("answer4")

    answer5 = data.get("answer5")

    answer6 = message.text

    my_list = find_resume(answer1, answer2, answer3, answer4, answer5, answer6)
    for i in my_list:
        await message.answer(i)
    await message.answer(f"Спасибо за использование бота\n"
                         f"\n{'/start для повтора'}")

    await state.finish()

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

