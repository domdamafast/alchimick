from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


# Все элементы и их названия для отображения в клавиатуре
ELEMENTS = {
    # начальные элементы
    "water": "💧 Вода",
    "air": "🌬 Воздух",
    "earth": "🌍 Земля",
    "fire": "🔥 Огонь",

    # старые крафты
    "steam": "💨 Пар",
    "lake": "🏞 Озеро",
    "rain": "🌧 Дождь",
    "sea": "🏝️ Море",
    "ocean": "⚓️ Океан",
    "dust": "🧹 Пыль",
    "fog": "🌫 Туман",
    "cloud": "☁️ Облако",
    "plant": "🌱 Растение",
    "tree": "🌳 Дерево",
    "forest": "🌲 Лес",
    "wave": "🌊 Волна",
    "storm": "🌪️ Шторм",
    "flame": "🐦‍🔥 Пламя",
    "lava": "🌋 Лава",
    "stone": "🪨 Камень",
    "metal": "🔩 Металл",

    # новые крафты
    "puddle": "💦 Лужа",
    "swamp": "🟫 Болото",
    "gas": "💨 Газ",
    "wind": "💨 Ветер",
    "heat": "♨️ Жара",
    "sky": "🌌 Небо",
    "mountain": "🏔 Гора",
    "volcano": "🌋 Вулкан",
    "snow": "❄️ Снег",
    "campfire": "🔥 Костёр",
    "ash": "⚫ Пепел",
    "mud": "🟤 Грязь",
    "grass": "🌿 Трава",
    "field": "🌾 Поле",
    "bread": "🍞 Хлеб",
    "rock": "🪨 Скала",
    "sand": "🏜 Песок",
    "glass": "🪟 Стекло",
    "ice": "🧊 Лёд",
    "window": "🪟 Окно",
    "salt": "🧂 Соль",
    "salt_water": "🧂🌊 Солёная вода",
    "mineral": "💎 Минерал",
    "energy": "⚡ Энергия",
    "machine": "🤖 Машина",
    "obsidian": "⬛ Обсидиан",
    "smooth_stone": "🪨 Гладкий камень",
    "tool": "🛠 Инструмент",
    "desert": "🏜 Пустыня",
    "island": "🏝 Остров",
}


# 4 элемента для начала игры
INITIAL_INVENTORY = ["water", "air", "earth", "fire"]


RECIPE_RESULTS = {
    # основные крафты
    frozenset(("water", "fire")): "steam",
    frozenset(("water", "earth")): "lake",
    frozenset(("steam", "air")): "rain",
    frozenset(("lake", "lake")): "sea",
    frozenset(("sea", "sea")): "ocean",

    # крафты 2 обновления
    frozenset(("earth", "air")): "dust",
    frozenset(("water", "air")): "fog",
    frozenset(("fog", "air")): "cloud",
    frozenset(("rain", "earth")): "plant",
    frozenset(("plant", "earth")): "tree",
    frozenset(("tree", "tree")): "forest",
    frozenset(("sea", "air")): "wave",
    frozenset(("wave", "wave")): "storm",
    frozenset(("fire", "air")): "flame",
    frozenset(("flame", "earth")): "lava",
    frozenset(("lava", "water")): "stone",
    frozenset(("stone", "fire")): "metal",

    # 30 дополнительных крафтов
    frozenset(("water", "water")): "puddle",
    frozenset(("puddle", "earth")): "swamp",
    frozenset(("swamp", "fire")): "gas",
    frozenset(("air", "air")): "wind",
    frozenset(("wind", "fire")): "heat",
    frozenset(("wind", "cloud")): "sky",
    frozenset(("earth", "earth")): "mountain",
    frozenset(("mountain", "fire")): "volcano",
    frozenset(("mountain", "air")): "snow",
    frozenset(("fire", "fire")): "campfire",
    frozenset(("campfire", "earth")): "ash",
    frozenset(("ash", "water")): "mud",
    frozenset(("plant", "water")): "grass",
    frozenset(("grass", "earth")): "field",
    frozenset(("field", "fire")): "bread",
    frozenset(("stone", "stone")): "rock",
    frozenset(("rock", "water")): "sand",
    frozenset(("sand", "fire")): "glass",
    frozenset(("glass", "water")): "ice",
    frozenset(("glass", "air")): "window",
    frozenset(("ocean", "fire")): "salt",
    frozenset(("salt", "water")): "salt_water",
    frozenset(("salt_water", "earth")): "mineral",
    frozenset(("storm", "fire")): "energy",
    frozenset(("energy", "metal")): "machine",
    frozenset(("lava", "air")): "obsidian",
    frozenset(("obsidian", "water")): "smooth_stone",
    frozenset(("smooth_stone", "metal")): "tool",
    frozenset(("sand", "sand")): "desert",
    frozenset(("sea", "earth")): "island",
}


TOTAL_ELEMENTS = len(ELEMENTS)


def user_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❓ Как играть")],
        ],
        resize_keyboard=True
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть", callback_data="play")],
            [InlineKeyboardButton(text="❓ Как играть", callback_data="how_to_play")],
        ]
    )


def inventory_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚗️ Крафт", callback_data="craft")]
        ]
    )


def craft_keyboard(inventory: list[str]) -> InlineKeyboardMarkup:
    buttons = []
    row = []

    for i, element_id in enumerate(inventory, start=1):
        row.append(
            InlineKeyboardButton(
                text=ELEMENTS[element_id],
                callback_data=f"craft_item:{element_id}"
            )
        )

        # каждые 3 кнопки — новая строка
        if i % 3 == 0:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="🎒 Инвентарь", callback_data="play")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
