from aiogram.types import \
    KeyboardButton, \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton

i1 = InlineKeyboardButton('👍',callback_data='i1')
i2 = InlineKeyboardButton('👎',callback_data='i2')
inlineKeyboard = InlineKeyboardMarkup().insert(i1).insert(i2)

b1 = KeyboardButton("Поделиться номером", request_location=True)
b2 = KeyboardButton("Больше не хочу никого искать", request_contact=True)
b3 = KeyboardButton("🙋‍♂️")

b1 = KeyboardButton("Найти собеседника")
b2 = KeyboardButton("Больше не хочу никого искать")
b3 = KeyboardButton("🙋‍♂️")

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(b1).add(b2).add(b3)
