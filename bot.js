require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');

const BOT_TOKEN = process.env.TELEGRAM_TOKEN;
const API_URL = process.env.PAIRING_API_URL;

const bot = new TelegramBot(BOT_TOKEN, { polling: true });

bot.onText(/\/pair (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const number = match[1];

    try {
        const response = await fetch(`${API_URL}${number}`);
        const data = await response.json();

        if (!data.code) {
            return bot.sendMessage(chatId, '❌ Could not generate code. Check the number format.');
        }

        await bot.sendMessage(chatId, `🔑 *Session Code for:* ${number}\n\`\`\`${data.code}\`\`\``, {
            parse_mode: 'Markdown'
        });

    } catch (err) {
        console.error("Error fetching code:", err);
        bot.sendMessage(chatId, '⚠️ Server error. Please try again later.');
    }
});
