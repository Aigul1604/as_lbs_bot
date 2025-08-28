import os
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("as_lbs_bot")

MAIN_KB = ReplyKeyboardMarkup(
    [["📥 Оставить заявку", "📞 Консультация"], ["📲 WhatsApp", "📋 Меню"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в AS-Lbs Customs Bot! Напишите ваш вопрос или выберите кнопку ниже.",
        reply_markup=MAIN_KB
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Команды: /start /help /id /ping /menu", reply_markup=MAIN_KB)

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ваш chat_id: {update.effective_chat.id}")

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ✅")

async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню:", reply_markup=MAIN_KB)

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if text == "📲 WhatsApp":
        await update.message.reply_text("Наш WhatsApp: https://wa.me/77022746433", reply_markup=MAIN_KB)
        return
    if text in ("📥 Оставить заявку", "📞 Консультация", "📋 Меню", "Меню"):
        await update.message.reply_text("Опишите, пожалуйста, ваш вопрос (товар/страна/Инкотермс/сроки).", reply_markup=MAIN_KB)
        return

    await update.message.reply_text("Спасибо! Ваша заявка принята. Мы свяжемся с вами.", reply_markup=MAIN_KB)

    if ADMIN_CHAT_ID:
        try:
            admin_id = int(ADMIN_CHAT_ID)
            user = update.effective_user
            name = user.full_name or (user.username or "клиент")
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"🆕 Заявка от {name} (@{user.username or '—'} | id {user.id}):\n{text}"
            )
        except Exception as e:
            log.warning(f"Не удалось отправить админу: {e}")

def main():
    if not TOKEN:
        raise SystemExit("[ERROR] TELEGRAM_BOT_TOKEN не задан в Environment Variables")

    app = Application.builder().token(TOKEN).build()

    # ✅ Без create_task: run_polling сам создаёт цикл и может удалить вебхук
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    log.info("Bot is running (polling, PTB v20)…")
    # drop_pending_updates=True удаляет возможный вебхук и старые апдейты БЕЗ ручного create_task
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
