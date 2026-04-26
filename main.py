import asyncio
import json
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

from keyboards import (
    ELEMENTS,
    INITIAL_INVENTORY,
    RECIPE_RESULTS,
    TOTAL_ELEMENTS,
    craft_keyboard,
    inventory_keyboard,
    main_menu_keyboard,
    user_keyboard,
)

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

DATA_FILE = "user_data.json"

user_inventories: dict[int, list[str]] = {}
craft_choices: dict[int, list[str]] = {}

ADMIN_USERNAMES = {"domdamafast"}


class RegisterState(StatesGroup):
    waiting_for_name = State()


def load_user_data() -> None:
    global user_inventories

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_inventories = {}
        return

    user_inventories = {
        int(user_id): [item for item in inventory if item in ELEMENTS]
        for user_id, inventory in data.items()
        if isinstance(inventory, list)
    }


def save_user_data() -> None:
    data = {
        str(user_id): inventory
        for user_id, inventory in user_inventories.items()
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def is_admin(message: Message) -> bool:
    admin_id = os.getenv("ADMIN_ID")

    if admin_id and str(message.from_user.id) == admin_id:
        return True

    username = message.from_user.username
    return username in ADMIN_USERNAMES


def get_inventory(user_id: int) -> list[str]:
    if user_id not in user_inventories:
        user_inventories[user_id] = INITIAL_INVENTORY.copy()
        save_user_data()
    return user_inventories[user_id]


def inventory_text(inventory: list[str]) -> str:
    items = [ELEMENTS[item] for item in inventory]

    rows = []
    row = []

    for i, item in enumerate(items, start=1):
        row.append(item)

        if i % 3 == 0:
            rows.append("    |    ".join(row))
            row = []

    if row:
        rows.append("    |    ".join(row))

    return (
        "🎒 Твой инвентарь:\n\n"
        + "\n".join(rows)
        + f"\n\nСобрано: {len(inventory)} из {TOTAL_ELEMENTS}"
    )


@dp.message(F.text == "❓ Как играть")
async def how_to_play_message(message: Message):
    await message.answer(
        "❓ Как играть:\n\n"
        "Соединяй элементы.\n"
        "Рецепты не показываются 😉\n"
        "Команда /reset сбрасывает твой прогресс.",
        reply_markup=user_keyboard()
    )


# 🔥 АДМИН — выдать все предметы
@dp.message(F.text.lower().in_({"add", "/add", "admin", "/admin"}))
async def admin_give_all_items(message: Message):
    if not is_admin(message):
        await message.answer("⛔ У тебя нет доступа к этой команде.")
        return

    user_id = message.from_user.id
    user_inventories[user_id] = list(ELEMENTS.keys())
    craft_choices[user_id] = []
    save_user_data()

    await message.answer(
        "👑 Тебе выданы все предметы.\n\n"
        f"Собрано: {TOTAL_ELEMENTS} из {TOTAL_ELEMENTS}",
        reply_markup=inventory_keyboard()
    )


#  СБРОС ТОЛЬКО СЕБЕ!!!!
@dp.message(F.text.lower().in_({"reset", "/reset"}))
async def reset_user_progress(message: Message):
    user_id = message.from_user.id

    if user_id in user_inventories:
        del user_inventories[user_id]

    if user_id in craft_choices:
        del craft_choices[user_id]

    save_user_data()

    await message.answer(
        "🗑 Твой прогресс сброшен.\n\n"
        "Нажми «Играть», чтобы начать заново.",
        reply_markup=main_menu_keyboard()
    )


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer("Введите имя:", reply_markup=user_keyboard())
    await state.set_state(RegisterState.waiting_for_name)


@dp.message(RegisterState.waiting_for_name)
async def save_name(message: Message, state: FSMContext):
    name = message.text

    await state.update_data(name=name)
    await state.clear()

    await message.answer(
        f"Привет, {name}! 🧪\nДобро пожаловать в игру Алхимия!",
        reply_markup=main_menu_keyboard()
    )


@dp.callback_query(F.data == "play")
async def play_button(callback: CallbackQuery):
    inventory = get_inventory(callback.from_user.id)
    craft_choices[callback.from_user.id] = []

    await callback.message.answer(
        inventory_text(inventory),
        reply_markup=inventory_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "craft")
async def craft_button(callback: CallbackQuery):
    inventory = get_inventory(callback.from_user.id)
    craft_choices[callback.from_user.id] = []

    await callback.message.answer(
        "⚗️ Крафт:\n\nВыбери два элемента.",
        reply_markup=craft_keyboard(inventory)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("craft_item:"))
async def craft_item_button(callback: CallbackQuery):
    user_id = callback.from_user.id
    inventory = get_inventory(user_id)
    element_id = callback.data.split(":", 1)[1]

    if element_id not in inventory:
        await callback.answer("Такого элемента пока нет.", show_alert=True)
        return

    choices = craft_choices.setdefault(user_id, [])
    choices.append(element_id)

    if len(choices) == 1:
        await callback.answer(f"Выбрано: {ELEMENTS[element_id]}")
        return

    first_item, second_item = choices
    craft_choices[user_id] = []

    result = RECIPE_RESULTS.get(frozenset((first_item, second_item)))

    if result is None:
        await callback.message.answer(
            f"❌ {ELEMENTS[first_item]} + {ELEMENTS[second_item]} — ничего не получилось."
        )
        await callback.answer()
        return

    if result in inventory:
        await callback.message.answer(
            f"✅ Уже есть: {ELEMENTS[result]}\n\n"
            f"Собрано: {len(inventory)} из {TOTAL_ELEMENTS}"
        )
        await callback.answer()
        return

    inventory.append(result)
    save_user_data()

    await callback.message.answer(
        f"🎉 Новый элемент: {ELEMENTS[result]}!\n\n"
        f"Собрано: {len(inventory)} из {TOTAL_ELEMENTS}",
        reply_markup=craft_keyboard(inventory)
    )
    await callback.answer()


@dp.callback_query(F.data == "how_to_play")
async def how_to_play_button(callback: CallbackQuery):
    await callback.message.answer(
        "❓ Как играть:\n\n"
        "Соединяй элементы.\n"
        "Рецепты не показываются 😉\n"
        "Команда /reset сбрасывает твой прогресс.",
        reply_markup=user_keyboard()
    )
    await callback.answer()


async def main():
    load_user_data()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
