import telebot
import math

# BotFather'dan olingan tokenni shu yerga qo'ying
BOT_TOKEN = "8987444695:AAHl-fEEWhoHilOaV_RBtK4QgopriXVAykk"
bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilar kiritgan raqamlarni vaqtincha saqlab turish uchun lug'at
user_data = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🚚 **Yuklarni Taqsimlash tizimiga xush kelibsiz!**\n\nJami yuk og'irligini kiriting (kg):")
    # Keyingi qadamga o'tish (get_weight funksiyasini chaqirish)
    bot.register_next_step_handler(message, get_weight)


def get_weight(message):
    chat_id = message.chat.id
    try:
        weight = float(message.text)
        user_data[chat_id] = {'weight': weight}  # Yukni saqlab qo'yamiz

        bot.send_message(chat_id, "🚛 Bitta mashina sig'imini kiriting (kg):")
        bot.register_next_step_handler(message, get_capacity)
    except ValueError:
        bot.send_message(chat_id, "❌ Iltimos, faqat raqam kiriting!\nJami yuk og'irligini qaytadan yozing:")
        bot.register_next_step_handler(message, get_weight)


def get_capacity(message):
    chat_id = message.chat.id
    try:
        capacity = float(message.text)
        weight = user_data[chat_id]['weight']  # Boyagi saqlangan yukni olamiz

        # Hisoblash mantig'i
        trucks = math.ceil(weight / capacity)

        # Chiroyli xabar tayyorlash
        report = (
            f"📋 **LOGISTIKA HISOBOTI**\n\n"
            f"📦 **Jami yuk:** {weight:,.0f} kg\n"
            f"🚚 **Mashina sig'imi:** {capacity:,.0f} kg\n"
            f"🔢 **Kerakli mashinalar:** {trucks} ta\n\n"
            f"Siz bilan ishlashdan mamnunmiz! 👍"
        )

        bot.send_message(chat_id, report, parse_mode="Markdown")

        # Ma'lumotlarni tozalab qo'yamiz
        user_data.pop(chat_id, None)

    except ValueError:
        bot.send_message(chat_id, "❌ Iltimos, faqat raqam kiriting!\nMashina sig'imini qaytadan yozing:")
        bot.register_next_step_handler(message, get_capacity)


# Botni doimiy eshitish rejimida ushlab turish
bot.polling(none_stop=True)