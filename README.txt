AS‑Lbs Telegram Bot — PTB v20 (fix event loop)

Исправлено падение: RuntimeError: no running event loop
Причина: create_task вызывался до запуска цикла.
Решение: использовать run_polling(drop_pending_updates=True) без ручного create_task.

Render (Background Worker):
- Build: pip3 install -r requirements.txt
- Start: python3 bot.py
- Env Vars:
  TELEGRAM_BOT_TOKEN = <токен>
  ADMIN_CHAT_ID      = <chat_id> (опционально)
