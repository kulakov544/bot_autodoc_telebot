import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards as kb
from get_data_site import get_data_site
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

#vin_car = ''
car_info = {'car_make': "марка машины",
            'model_car': "модель машины",
            'year_car': "год выпуска"
            }


class Vin(StatesGroup):
    vin_car = State()



# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    await message.reply(f"Привет. \n Твой ID: {user_id}\nИмя: {user_name}.", reply_markup=kb.start)

@dp.callback_query(Command('vin'))
async def start_script(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Vin.vin_car)
    await callback.message.answer(f"Введите ваш VIN номер:")









# Обработчик текстовых сообщений
@dp.message(F.text)
async def user_text_vin(message: types.Message):
    global vin_car
    vin_car = message.text
    await message.reply(f"Ваш VIN номер: {vin_car}", reply_markup=kb.start)


@dp.message()
async def car_info(message: types.Message):
    global car_info
    await message.reply(f"Ваш VIN номер: {car_info}", reply_markup=kb.start)

@dp.message()
async def user_text_vin_answer(message: types.Message):
    global vin_car
    await message.answer(vin_car, reply_markup=kb.start)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

# https://www.autodoc.ru/catalogs/original/list-nodes/nodes?vin=WAUBH54B11N111054


# vin = 'WAUBH54B11N111054'

# get_data_site(vin)
