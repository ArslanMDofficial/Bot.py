import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Pair command handler
async def pair_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract number from the command
        args = context.args
        if not args or len(args[0]) < 10:
            await update.message.reply_text(
                "❌ *Invalid Format!*\n\n✅ *Example:* `/pair 923477868XXX`",
                parse_mode="Markdown"
            )
            return

        number = args[0]

        # Call external API
        api_url = "https://sarkar-md-session-generator.koyeb.app/code?number={number}"
        response = requests.get(api_url)
        data = response.json()

        # Check if code is present
        if not data.get("code"):
            await update.message.reply_text(
                "❌ Failed to generate pairing code!\n\nPlease check the number format.",
                parse_mode="Markdown"
            )
            return

        pairing_code = data["code"]

        # Send the pairing code
        await update.message.reply_text(
            f"```\n{pairing_code}\n```",
            parse_mode="Markdown"
        )

        # Follow-up message
        await update.message.reply_text(
            f"🔐 *Pairing Code Generated!*\n\n📱 *For Number:* `{number}`\n✨ *Code sent above*",
            parse_mode="Markdown"
        )

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text(
            "⚠️ *Server Error!*\n\nPlease try again later.",
            parse_mode="Markdown"
        )

# Start the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("pair", pair_command))

    print("🤖 Bot is running...")
    app.run_polling()
