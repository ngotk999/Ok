import os
import re
import time
import subprocess
import threading
from flask import Flask
import telebot
from telebot import types

# ==== CẤU HÌNH TOKEN ====
BOT_TOKEN = "7797658812:AAH_tyChkSFoZIfeCP-BB5naqRpprsqKUfw"  # ← thay bằng token thật từ @BotFather
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ==== FLASK GIỮ BOT SỐNG TRÊN RENDER ====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

# ==== BIẾN TOÀN CỤC CHỐNG SPAM ====
cooldown_dict = {}
last_spam_time = {}

# ==== LỆNH /spamvip ====
@bot.message_handler(commands=['spamvip'])
def spam_vip_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"
    full_name = message.from_user.full_name

    if len(message.text.split()) < 2:
        bot.reply_to(message, '📞 Vui lòng nhập số điện thoại.')
        return

    phone_number = message.text.split()[1]

    if not re.search(r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, '❌ Số điện thoại không hợp lệ!')
        return

    current_time = time.time()
    if phone_number in last_spam_time:
        time_since_last_spam = current_time - last_spam_time[phone_number]
        if time_since_last_spam < 600:
            remaining_time = int(600 - time_since_last_spam)
            bot.reply_to(message, f'⚠️ Số {phone_number} đã được spam. Đợi {remaining_time} giây.')
            return

    last_spam_time[phone_number] = current_time
    cooldown_dict[username] = {'vip': current_time}

    # Gửi video xác nhận
    video_url = "https://files.catbox.moe/xbgx14.mp4"
    caption = f"""<blockquote> cái địt mẹ mày thằng {full_name}
Attack Sent by : @{username}
Gửi yêu cầu tấn công thành công 🚀
Số tấn công 📱: [ {phone_number} ]
Số lượt Tấn công 📱: [ 50 Lần ]
Plan Của Bạn : [ VIP ] 
Tên người dùng 👤: [ {full_name} ]
</blockquote>"""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"))
    bot.send_video(message.chat.id, video_url, caption=caption, parse_mode="HTML", reply_markup=keyboard)

    sent = bot.reply_to(message, "Đang xử lý...")
    loading_frames = ["Buy GÌ Cứ Ib @ngotk999 đi", "cái địt mẹ mày đang loading..."]
    for frame in loading_frames:
        try:
            bot.edit_message_text(frame, chat_id=message.chat.id, message_id=sent.message_id)
            time.sleep(0.4)
        except:
            pass

    # Gọi các script spam
    script_files = ["text1.py", "text2.py", "text3.py", "text4.py", "text5.py",
                    "text6.py", "text7.py", "text8.py", "text9.py", "text10.py"]

    for script_file in script_files:
        script_path = os.path.join(os.getcwd(), script_file)
        try:
            subprocess.Popen(["python", script_path, phone_number, "50"])
        except Exception as e:
            print(f"Lỗi khi chạy {script_file}: {e}")

    try:
        bot.edit_message_text(f"[{full_name}] Bắt đầu spam {phone_number}!", chat_id=message.chat.id, message_id=sent.message_id)
        time.sleep(1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, sent.message_id)
    except:
        pass

# ==== KHỞI ĐỘNG BOT ====
print("🤖 Bot đã sẵn sàng!")
bot.infinity_polling()
