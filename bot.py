# -*- coding: utf-8 -*-
"""
Қарапайым Telegram бот.
- /start  : ботты тексеру
- /help   : қысқа көмек
- /ping   : "pong" деп жауап береді
- Кез келген мәтін: иесіне (OWNER_ID) echo ретінде қайта жібереді
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# >>> Осында өз мәндеріңді қой:
BOT_TOKEN = "8370951983:AAGMMIEeTA0D-xA14JN4kkxjIO_2pKbUR6g"   # BotFather берген токенді қой
OWNER_ID  =  5381443968                              # userinfobot берген user id (мысалы: 5381443968)

# ----------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("smartmoney-bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Старт командасы."""
    user = update.effective_user
    if OWNER_ID and user and user.id != OWNER_ID:
        await update.message.reply_text("Сәлем! Бұл жеке бот. Рұқсат жоқ.")
        return

    await update.message.reply_text(
        "✅ Бот іске қосылды!\n"
        "Командалар: /help, /ping\n"
        "Мәтін жіберсең — саған echo жасап қайта жібереді."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ℹ️ Командалар:\n"
        "/start — ботты тексеру\n"
        "/ping — жылдам жауап\n"
        "Кез келген мәтінді жібер — echo аласың."
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("pong")


async def echo_owner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Иеден келсе — echo; басқа қолданушыдан келсе — рұқсат жоқ деп жауап."""
    msg = update.effective_message
    user = update.effective_user

    if OWNER_ID and user and user.id != OWNER_ID:
        await msg.reply_text("Бұл жеке бот. Рұқсат жоқ.")
        return

    # Қарапайым echo
    if msg.text:
        await msg.reply_text(f"🔁 {msg.text}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Қате:", exc_info=context.error)


async def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN.startswith("PASTE_"):
        raise RuntimeError("BOT_TOKEN орнатылмаған! bot.py ішінде BOT_TOKEN-ге өз токеніңді қой.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_owner))
    app.add_error_handler(error_handler)

    # Polling режимі
    logger.info("Бот іске қосылып жатыр…")
    await app.initialize()
    await app.start()
    logger.info("Бот жұмыс істеп тұр. Тоқтату үшін Ctrl+C бас.")
    try:
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await asyncio.Event().wait()  # мәңгі күтеді (Ctrl+C тоқтатады)
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот тоқтатылды.")
