from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Привет. \n Твой ID: {message.from_user.id}\n-Имя: {message.from_user.first_name}",
                        reply_markup=kb.main)

# Обработчик текстовых сообщений
@router.message_handler(content_types=['text'])
async def handle_text(message: types.Message):
    global vin_car
    vin_car = message.text
    await message.reply(f"Received your input: {vin_car}")

@router.message(F.text == "1")
async def keyboard_settings(message: Message):
    await message.reply('Список деталей:', reply_markup=kb.settings)

@router.message(F.text == "2")
async def keyboard_inline_cars(message: Message):
    await message.reply('клавиатура inline_cars', reply_markup=await kb.inline_cars())

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('это команда /help')

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

# @dp.message(Command)
# async def get_photo(message: Message):
#     await message.answer_photo(photo ='тут id фото или ссылка', caption='описание фото')

@router.message(F.text == "Как дела?")
async def how_are_you(message: Message):
    await message.answer("Ok!")

