import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_URL = "https://knoxxyop-num-info-api.vercel.app/lookup?number="

def strip_owner(data):
    # Remove only the unwanted owner field
    data.pop("Buy Api", None)
    return data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /num <number> to look up info (raw JSON).")

async def lookup_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /num <number>")
        return

    number = context.args[0].strip()
    if not number.isdigit():
        await update.message.reply_text("Please send a valid number.")
        return

    response = requests.get(API_URL + number)
    if response.status_code != 200:
        await update.message.reply_text("API error or invalid response.")
        return

    data = response.json()
    cleaned = strip_owner(data)

    # Pretty-print JSON for Telegram
    reply = json.dumps(cleaned, indent=2, ensure_ascii=False)
    await update.message.reply_text(f"```json\n{reply}\n```", parse_mode="MarkdownV2")

def main():
    app = ApplicationBuilder().token("8385605894:AAEory3fEggMYu8907UzczHNH-tMAtsf64s").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", lookup_number))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
