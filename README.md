# 🧪 Alchemy Bot
Alchemy Bot is a Telegram game where you combine elements to discover new ones. Start with water, air, earth, and fire, experiment with crafting, and unlock over 50 unique elements. Progress is saved automatically, and every discovery expands your possibilities.
🎮 How to Play
You start with basic elements:
💧 Water
🌬 Air
🌍 Earth
🔥 Fire
Combine elements together
If the combination is correct — you unlock a new element
New elements can be used in further crafting
❗ Recipes are not shown — you have to figure them out yourself
⚗️ Features
🔹 50+ elements
🔹 Crafting system
🔹 Discover new elements
🔹 Progress saving (even after bot restart)
🔹 User-friendly button interface
🔹 Inventory displayed in 3 columns
🔹 Admin commands
🔹 Progress reset (/reset)

Getting Started
Install dependencies:
pip install aiogram python-dotenv

Create .env file(without quotes''):
BOT_TOKEN=your_bot_token
ADMIN_ID=your_id (optional)

Run the bot:
python main.py

project/
│
├── main.py          # bot logic
├── keyboards.py     # keyboards and crafting system
├── user_data.json   # user progress storage(no need to download anything, this file appears automatically)
└── .env             # bot token

Commands
/start — start the game
/reset — reset your progress
admin, add — get all elements (admin only)

