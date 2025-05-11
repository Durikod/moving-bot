📌 Инструкция по запуску бота на телефоне через Render:

1. Перейди на https://github.com и создай репозиторий (например: moving-bot)
2. Зайди в репозиторий → нажми "Add file" → "Upload files"
3. Распакуй этот архив и загрузи все файлы: moving_bot.py, requirements.txt, README.txt
4. Нажми "Commit changes"

🔧 Теперь на https://render.com:
1. Создай аккаунт и нажми "New" > "Web Service"
2. Подключи GitHub и выбери свой репозиторий
3. В настройках Render укажи:
   - Environment: Python
   - Build command: pip install -r requirements.txt
   - Start command: python moving_bot.py
   - Python version: 3.10

Бот будет работать постоянно 🚀
