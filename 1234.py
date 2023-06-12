from __future__ import annotations

import logging
from tkn import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from qwerty import inlineKeyboard
from qwerty import keyboard

TOKEN = TOKEN
print('e')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

connected_users = []
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    is_banned = data.get('is_banned', False)
    if is_banned:
        return
    await message.reply(text="Hi!\nI'm ZXCbot!\nPowered by aiogram.\n Tell me your name.", reply_markup=keyboard)
    await state.set_state('q1')


@dp.message_handler(state="q1")
async def process(message: types.Message, state: FSMContext):
    name = message.text

    await state.update_data({"name": name})
    await state.set_state("q2")
    await message.answer("Tell me your age")


@dp.message_handler(state="q2")
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data({"age": int(age)})
        await state.set_state("echo")
        await message.answer("Now I am echo-bot!", reply_markup=inlineKeyboard)
        connected_users.append(message.from_user.id)
    else:
        await message.answer("This is not a number, try another time")
        data = await state.get_data()
        await message.answer(f"This is not a number, try another time {data['name']}")
    if int(age) < 18:
        await message.answer('sorry, i cant work with you')
        await state.set_data({
            "is_banned": True
        })
        connected_users.append(message.from_user.id)
        await bot.send_chat_action(message.from_user.id, types.ChatActions.TYPING)


waiting_users: set[int] = set()


@dp.message_handler(commands=['find'], state='find')
async def find_process(message: types.Message, state: FSMContext):
    await message.answer("Поиск собеседника...")
    current_user = message.from_user.id
    waiting_users.add(current_user)
    waiting_users.add(message.from_user.id)
    await message.answer(waiting_users)

    if len(waiting_users) >= 2:
        for another_user in waiting_users:
            if another_user == current_user:
                continue
            else:
                break
        waiting_users.remove(current_user)
        waiting_users.remove(another_user)

        another_user_state = dp.current_state(chat=another_user, user=another_user)

        await state.set_state("chatting")
        await another_user_state.set_state("chatting")

        await state.update_data({"target": another_user})
        await another_user_state.update_data({"target": current_user})

        await bot.send_message(current_user, "Найден собеседник! Начинайте общаться")
        await bot.send_message(another_user, "Найден собеседник! Начинайте общаться")

    @dp.message_handler(state='chatting')
    async def chatting_proc(message: types.Message, state: FSMContext):
        another_user_data = await state.get_data()
        another_user = another_user_data['target']
        await bot.send_message(another_user, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
