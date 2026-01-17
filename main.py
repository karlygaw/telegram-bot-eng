from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Update
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

app = FastAPI()

# ---------- КНОПКИ ----------

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👶 Для детей", callback_data="kids"),
            InlineKeyboardButton(text="🧑 Для взрослых", callback_data="adults")
        ],
        [
            InlineKeyboardButton(text="ℹ️ О школе", callback_data="about")
        ]
    ])

def level_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Начальный", callback_data="level_beginner"),
            InlineKeyboardButton(text="A2", callback_data="level_a2"),
            InlineKeyboardButton(text="B1", callback_data="level_b1")
        ],
        [
            InlineKeyboardButton(text="❓ Не знаю уровень", callback_data="level_unknown")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")
        ]
    ])

def format_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Групповые занятия", callback_data="group"),
            InlineKeyboardButton(text="👤 Индивидуальные занятия", callback_data="individual")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_level")
        ]
    ])

def finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📞 Записаться на пробный урок", callback_data="trial")
        ],
        [
            InlineKeyboardButton(text="⬅️ Начать заново", callback_data="restart")
        ]
    ])

# ---------- СТАРТ ----------

@dp.message(commands=["start"])
async def start(message: Message):
    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Я виртуальный помощник школы английского языка.\n"
        "Я помогу вам выбрать подходящий курс и ответить на вопросы.\n\n"
        "Кого вы хотите записать на занятия?",
        reply_markup=start_keyboard()
    )

# ---------- О ШКОЛЕ ----------

@dp.callback_query(lambda c: c.data == "about")
async def about_school(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ **О нашей школе**\n\n"
        "📌 Обучаем детей и взрослых\n"
        "📌 Маленькие группы до 6 человек\n"
        "📌 Онлайн и офлайн занятия\n"
        "📌 Бесплатное определение уровня\n\n"
        "Выберите, с чего хотите начать:",
        reply_markup=start_keyboard()
    )
    await callback.answer()

# ---------- ДЕТИ / ВЗРОСЛЫЕ ----------

@dp.callback_query(lambda c: c.data in ["kids", "adults"])
async def choose_type(callback: CallbackQuery):
    await callback.message.edit_text(
        "Отлично! 😊\n\n"
        "Выберите уровень английского:",
        reply_markup=level_keyboard()
    )
    await callback.answer()

# ---------- УРОВЕНЬ ----------

@dp.callback_query(lambda c: c.data.startswith("level_"))
async def choose_level(callback: CallbackQuery):
    await callback.message.edit_text(
        "Спасибо за выбор! 📘\n\n"
        "🗓 Занятия: 3 раза в неделю\n"
        "⏰ Время подбирается индивидуально\n"
        "💰 Стоимость: 3000 ₸ за занятие\n\n"
        "Какой формат занятий вам подходит?",
        reply_markup=format_keyboard()
    )
    await callback.answer()

# ---------- НАЗАД К СТАРТУ ----------

@dp.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    await callback.message.edit_text(
        "Кого вы хотите записать на занятия?",
        reply_markup=start_keyboard()
    )
    await callback.answer()

# ---------- НАЗАД К УРОВНЮ ----------

@dp.callback_query(lambda c: c.data == "back_to_level")
async def back_to_level(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите уровень английского:",
        reply_markup=level_keyboard()
    )
    await callback.answer()

# ---------- ФОРМАТ ----------

@dp.callback_query(lambda c: c.data in ["group", "individual"])
async def choose_format(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 Отличный выбор!\n\n"
        "📍 Следующий шаг — пробный урок\n"
        "На нём мы определим уровень и подберём преподавателя.\n\n"
        "Хотите записаться?",
        reply_markup=finish_keyboard()
    )
    await callback.answer()

# ---------- ПРОБНЫЙ УРОК ----------

@dp.callback_query(lambda c: c.data == "trial")
async def trial(callback: CallbackQuery):
    await callback.message.edit_text(
        "📞 Спасибо за интерес к обучению!\n\n"
        "Пожалуйста, напишите ваш номер телефона или ожидайте, "
        "администратор свяжется с вами в ближайшее время.\n\n"
        "Будем рады видеть вас на занятиях 😊"
    )
    await callback.answer()

# ---------- ПЕРЕЗАПУСК ----------

@dp.callback_query(lambda c: c.data == "restart")
async def restart(callback: CallbackQuery):
    await callback.message.edit_text(
        "Давайте начнём сначала 😊\n\n"
        "Кого вы хотите записать на занятия?",
        reply_markup=start_keyboard()
    )
    await callback.answer()

# ---------- ЗАПУСК ----------

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
def health():
    return {"status": "ok"}
