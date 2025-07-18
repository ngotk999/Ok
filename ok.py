import logging
import requests
import threading
import time
import re
#
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

#config

#Log setup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ADMIN_ID = 6043728545
TOKEN = "7993764210:AAGnM45yo0rRwqHoRh7pN5W-C10NdJ-b8QI"

allowed_group_id = -1002403107765

async def lenh_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or "bạn"

    caption = f"""<blockquote> 🚀📖⭐BOT SPAM CALL + SMS⭐📖🚀 </blockquote>
<b>tăng Like/Follow Hệ Thống Seeding Mạng Xã Hội Việt Nam 
🌐 https://learncodehub.click 🌐</b> 

<blockquote expandable>📖

18 câu lệnh dành cho người dùng

⭐ Lệnh khởi đầu
» /start: Lệnh khởi đầu 
⚔️ Lệnh Spam
» /getkey: Để lấy key ngày 
» /key: Để nhập key ngày
» /spam: Spam 30 
» /spamvip: Spam 200 

🔰 Lệnh tiện ích
» /admin: Thông tin admin 
» /qr: Tạo QR của chữ
» /voice: Đổi văn bản thành giọng nói
» /time: Xem thời gian bot hoạt động 
» /info: Lấy ID người dùng 
» /check: Check web hoạt động  
» /html: Lấy code web
» /avtfb : Lấy avatar FB xuyên khiên
</blockquote> 
<b>[🚀] Lệnh Cho Riêng @{username}</b> 
<blockquote expandable>📖

» /add: Thêm người dùng spamvip 

</blockquote>"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),
            InlineKeyboardButton("🤖 Bot", url="https://t.me/SpamSmsCallokok_bot")
        ]
    ])

    video_url = "https://files.catbox.moe/08c1q8.mp4"

    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=video_url,
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )

async def spamvip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra nếu tin nhắn được gửi từ nhóm hợp lệ
    chat_id = update.message.chat_id
    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Bot chỉ có thể hoạt động trong nhóm này!",
        )
        return
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Không xác định"
    message_id = update.message.message_id
    current_time = time.time()

    # Kiểm tra quyền truy cập
    if user_id not in allowed_users:
        await update.message.reply_text(
            "<blockquote><b>Sử dụng /napvip để nạp và sử dụng spamvip</b></blockquote>",
            parse_mode="HTML",
        )
        return

    # Kiểm tra cooldown (30 giây)
    if username in cooldown_dict and current_time - cooldown_dict[username].get("free", 0) < 30:
        remaining_time = int(30 - (current_time - cooldown_dict[username].get("free", 0)))
        await update.message.reply_text(
            f"<blockquote>@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /spamvip.</blockquote>",
            parse_mode="HTML",
        )
        return

    # Cập nhật thời gian cooldown
    cooldown_dict[username] = {"free": current_time}

    # Phân tích cú pháp lệnh
    params = context.args
    if len(params) < 2:
        await update.message.reply_text("Thiếu thông tin (VD: /spamvip 0987654321 100).")
        return

    phone_number = params[0]
    try:
        num_spams = int(params[1])
        if num_spams < 20 or num_spams > 200:
            await update.message.reply_text("Số lần spam phải lớn hơn 20 và nhỏ hơn 200.")
            return
    except ValueError:
        await update.message.reply_text("Số lần spam không hợp lệ. Vui lòng nhập số nguyên lớn hơn 20.")
        return

    # Kiểm tra số điện thoại admin
    if phone_number in ["03939456755"]:
        await update.message.reply_text("Bot của anh nên anh sẽ không bị spam =))")
        return

    # Thông tin spam
    name_bot = "@KLTOOLBOT"
    admin = "@ngotk999"
    today = datetime.now().strftime("%Y-%m-%d")
    video_url = "https://files.catbox.moe/08c1q8.mp4"

    # Nội dung gửi đi
    message_text = f'''
<b>                          🚀   BOT BY 
  TẤN KIỆT  🚀</b>
<blockquote><b>┌──────────⭓
│»👾{name_bot}
│»👤USER: @{username}                      
│»SPAM: 🚀SUCCESS🚀
│»GÓI🔰: ⭐VIP⭐
│»📞PHONE: {phone_number}
│»✈ADMIN: {admin}
│»⚔️INTERACTIONS: {num_spams}
│»📅TODAY : {today}
└───────────────[✓]
</b></blockquote>
'''

    # Gửi video kèm nội dung
    try:
        await update.message.reply_video(
            video=video_url,
            caption=message_text,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Lỗi khi gửi video: {e}")
        await update.message.reply_text(
            "<blockquote><b>Không thể gửi video. Vui lòng thử lại sau.</b></blockquote>",
            parse_mode="HTML"
        )
        return

    # Tiến hành spam bằng subprocess
    file_path = os.path.join(os.getcwd(), "sm.py")
    try:
        process = subprocess.Popen(["python", file_path, phone_number, str(num_spams)])
        logging.info(f"Đã khởi chạy spam trên {phone_number} với {num_spams} lần.")
    except Exception as e:
        logging.error(f"Lỗi khi khởi chạy quá trình spam: {e}")

# Thêm handler cho lệnh /spamvip
app.add_handler(CommandHandler("spamvip", spamvip_command))

VIP_FILE = "vip_users.json"

def load_allowed_users():
    if os.path.exists(VIP_FILE):
        with open(VIP_FILE, "r") as f:
            return json.load(f)
    return []

def save_allowed_users(user_list):
    with open(VIP_FILE, "w") as f:
        json.dump(user_list, f)

async def addvip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text(
            "<blockquote><b>Tuổi gì đòi add</b></blockquote>",
            parse_mode="HTML"
        )
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "<blockquote><b>ID đâu @ngotk999</b></blockquote>",
            parse_mode="HTML"
        )
        return

    user_id = int(context.args[0])

    if user_id in allowed_users:
        await update.message.reply_text(
            f"<blockquote><b>ID này đã được cấp từ trước rồi: {user_id}</b></blockquote>",
            parse_mode="HTML"
        )
        return

    allowed_users.append(user_id)
    save_allowed_users(allowed_users)

    await update.message.reply_text(
        f"<blockquote><b>Người dùng {user_id} đã được cấp quyền sử dụng /spamvip 🌠</b></blockquote>",
        parse_mode="HTML"
    )

app.add_handler(CommandHandler("addvip", addvip_command))

async def delvip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text(
            "<blockquote><b>Bạn không có quyền thực hiện lệnh này.</b></blockquote>",
            parse_mode="HTML"
        )
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "<blockquote><b>Vui lòng nhập ID người dùng cần xóa.</b></blockquote>",
            parse_mode="HTML"
        )
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "<blockquote><b>ID không hợp lệ.</b></blockquote>",
            parse_mode="HTML"
        )
        return

    if user_id not in allowed_users:
        await update.message.reply_text(
            "<blockquote><b>ID này không nằm trong danh sách VIP.</b></blockquote>",
            parse_mode="HTML"
        )
        return

    allowed_users.remove(user_id)
    save_allowed_users(allowed_users)

    await update.message.reply_text(
        f"<blockquote><b>Đã xóa {user_id} khỏi danh sách VIP.</b></blockquote>",
        parse_mode="HTML"
    )

app.add_handler(CommandHandler("delvip", delvip_command))
# Xóa hàm bot tắt và các phần kiểm tra trạng thái bot

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

# Ghi lại thời điểm bot khởi động
bot_start_time = datetime.utcnow()

# Hàm tạo ảnh chứa thời gian uptime
def create_uptime_image():
    now = datetime.utcnow()
    uptime = now - bot_start_time
    minutes, seconds = divmod(int(uptime.total_seconds()), 60)
    uptime_str = f"{minutes:02}:{seconds:02}"

    # Tạo ảnh nền đen như ảnh mẫu
    img = Image.new("RGB", (1280, 720), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    # Font mặc định, bạn có thể thay bằng font .ttf nếu có file
    try:
        font_big = ImageFont.truetype("arial.ttf", 120)
        font_timer = ImageFont.truetype("arial.ttf", 100)
        font_label = ImageFont.truetype("arial.ttf", 40)
    except:
        font_big = font_timer = font_label = ImageFont.load_default()

    # Viết "TÁN KIỆT"
    draw.text((400, 250), "TÁN KIỆT", font=font_big, fill=(255, 100, 100))

    # Viết timer
    draw.rectangle((500, 500, 780, 600), fill=(255, 255, 255))
    draw.text((520, 510), uptime_str, font=font_timer, fill=(255, 0, 0))

    # Viết "TIMEBOT"
    draw.text((50, 600), "TIMEBOT", font=font_label, fill=(255, 255, 255))

    # Kết xuất thành buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Hàm xử lý lệnh /time
async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_buffer = create_uptime_image()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_buffer,
        caption="🕒 Thời gian hoạt động bot",
    )
    
app.add_handler(CommandHandler("time", time_command))

import locale
from datetime import datetime

from datetime import datetime

def format_date_vietnamese(date):
    weekdays = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Năm", "Thứ sáu", "Thứ bảy", "chủ nhật"]
    months = ["tháng 1", "tháng 2", "tháng 3", "tháng 4", "tháng 5", "tháng 6", 
              "tháng 7", "tháng 8", "tháng 9", "tháng 10", "tháng 11", "tháng 12"]
    weekday = weekdays[date.weekday()]
    month = months[date.month - 1]
    return f"{weekday}, {date.day} {month} năm {date.year}"

today = format_date_vietnamese(datetime.now())
print(today)  # In kết quả ngày hiện tại

async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra nếu tin nhắn được gửi từ nhóm hợp lệ
    chat_id = update.message.chat_id
    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Bot chỉ có thể hoạt động trong nhóm này https://t.me/Spamsmstracuuttvip",
        )
        return
    
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Không xác định"
    current_time = time.time()

    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "<blockquote><b>VUI LÒNG NHẬP SỐ ĐIỆN THOẠI VÀ SỐ LƯỢNG TIN NHẮN</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    phone_number = args[0]
    if not phone_number.isnumeric():
        await update.message.reply_text(
            "<blockquote><b>SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ!</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    try:
        repeat_count = int(args[1])
    except ValueError:
        await update.message.reply_text(
            "<blockquote><b>SỐ LƯỢNG TIN NHẮN PHẢI LÀ MỘT SỐ NGUYÊN</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    if repeat_count <= 0 or repeat_count > 30:
        await update.message.reply_text(
            "<blockquote><b>SỐ LƯỢNG TIN NHẮN PHẢI TỪ 1 ĐẾN 30.</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    # Danh sách số điện thoại bị cấm
    banned_numbers = ['113', '911', '114', '115', '+843929456755', '03994526755', '09285721953', '+849285721953']
    if phone_number in banned_numbers:
        await update.message.reply_text(
            "<blockquote><b>Yêu admin à mà spam</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    # Gửi video kèm theo nội dung
    file_path = os.path.join(os.getcwd(), "sm.py")
    try:
        process = subprocess.Popen(["python", file_path, phone_number, str(repeat_count)])
    except Exception as e:
        logging.error(f"Error starting spam process: {e}")
        await update.message.reply_text(
            "<blockquote><b>Có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại sau.</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    # Ghi lại thời gian để quản lý cooldown
    cooldown_dict[username] = {'free': current_time}

    # Lấy ngày hôm nay với định dạng tiếng Việt
    today = datetime.now().strftime("%A, %d tháng %m năm %Y")  # Thứ Ngày tháng năm

    # Đường dẫn video và nội dung gửi đi
    video_url = "https://files.catbox.moe/08c1q8.mp4"
    message_text = f'''
<b>                          🚀   BOT BY 
  TẤN KIỆT  🚀</b>
<blockquote><b>┌──────────⭓
│»👾@KLTOOLBOT
│»👤USER: @{username}                      
│»SPAM: 🚀SUCCESS🚀
│»GÓI🔰: ⭐FREE⭐
│»📞PHONE: {phone_number}
│»✈ADMIN: @ngotk999
│»⚔️INTERACTIONS: {repeat_count}
│»📅TODAY : {today}
└───────────────[✓]
</b></blockquote>
'''
    try:
        await update.message.reply_video(
            video_url,
            caption=message_text,
            parse_mode='HTML'
        )
    except Exception as e:
        logging.error(f"Error sending video: {e}")
        await update.message.reply_text(
            "<blockquote><b>Không thể gửi video. Vui lòng thử lại sau.</b></blockquote>", 
            parse_mode='HTML'
        )

async def handle_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"ID của bạn là: <code>{update.effective_user.id}</code>",
        parse_mode="HTML"
    )

async def handle_tt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    waiting = None
    try:
        if len(context.args) < 1:
            await update.message.reply_text("Vui lòng cung cấp username TikTok sau lệnh /tt.")
            return

        unique_id = context.args[0]
        waiting = await update.message.reply_text("⌛️")

        res = requests.get(f"https://azig.dev/tiktok?info={unique_id}")
        data = res.json()

        if data['code'] == 0:
            user = data['data']['user']
            stats = data['data']['stats']
            tiktok_link = f"https://www.tiktok.com/@{user['uniqueId']}"

            caption = f"""
<blockquote>
👤 <b>TikTok Info</b>

📛 <b>Username:</b> <a href='{tiktok_link}'>{user['uniqueId']}</a>  
🆔 <b>ID:</b> <code>{user['id']}</code>  
📍 <b>Nickname:</b> {user['nickname']}  
📝 <b>BIO:</b> <code>{user['signature']}</code>  
✅ <b>Verified:</b> {'Đã xác minh' if user['verified'] else 'Chưa xác minh'}  
👥 <b>Followers:</b> <code>{stats['followerCount']}</code>  
👣 <b>Following:</b> <code>{stats['followingCount']}</code>  
❤️ <b>Likes:</b> <code>{stats['heartCount']}</code>  
🎥 <b>Videos:</b> <code>{stats['videoCount']}</code>  
👍 <b>Diggs:</b> <code>{stats['diggCount']}</code>
</blockquote>
"""

            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=user['avatarMedium'],
                caption=caption,
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text("Không tìm thấy thông tin TikTok.")

    except Exception as e:
        logger.error(str(e))
        await update.message.reply_text("Đã xảy ra lỗi khi xử lý.")

    finally:
        # Xóa tin nhắn chờ nếu có
        if waiting:
            try:
                await context.bot.delete_message(update.effective_chat.id, waiting.message_id)
            except:
                pass

sent_messages = []

def delete_messages(chat_id, bot):
    time.sleep(60)
    for mid in sent_messages:
        try:
            bot.delete_message(chat_id, mid)
        except:
            pass
    sent_messages.clear()

# 📽️ /vdgai
async def handle_video_gai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = await update.message.reply_text("⏳")
    try:
        res = requests.get("https://apiquockhanh.click/video/videogai").json()
        url = res.get("url")

        if url:
            user = update.effective_user.username or "Không tên"
            caption = f"<blockquote>Xem Gái Lắm @{user}</blockquote>"
            video_msg = await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=url,
                caption=caption,
                parse_mode='HTML'
            )
            sent_messages.append(video_msg.message_id)
        else:
            await update.message.reply_text("Không tìm thấy video.")
    except Exception as e:
        await update.message.reply_text("Lỗi API.")
    finally:
        try:
            await context.bot.delete_message(update.effective_chat.id, status.message_id)
        except:
            pass

# 📽️ /anime
async def handle_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Đang lấy video...⌛")
    try:
        res = requests.get("https://apiquockhanh.click/video/videoanime", timeout=5).json()
        url = res.get("url")

        if url:
            video_msg = await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=url,
                caption="🎬 Video anime ngẫu nhiên 🎥"
            )
            sent_messages.append(video_msg.message_id)
        else:
            await update.message.reply_text("Không thể lấy video anime.")
    except Exception as e:
        await update.message.reply_text("API lỗi.")
    finally:
        try:
            await context.bot.delete_message(update.effective_chat.id, msg.message_id)
        except:
            pass

async def handle_gai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🔎 Đang tìm kiếm ảnh...")
    sent_messages.append(msg.message_id)

    try:
        res = requests.get("https://subhatde.id.vn/images/gai").json()
        url = res.get("url")

        if url:
            caption = f"Ảnh bạn yêu cầu, @{update.effective_user.username}"
            m = await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=url,
                caption=caption
            )
            sent_messages.append(m.message_id)

            # Gọi hàm xóa tin nhắn sau 60s
            threading.Thread(
                target=delete_messages,
                args=(update.effective_chat.id, context.bot)
            ).start()
        else:
            await update.message.reply_text("API không trả ảnh.")
    except Exception as e:
        await update.message.reply_text("Lỗi: " + str(e))

async def handle_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_url = "https://files.catbox.moe/08c1q8.mp4"
    username = update.effective_user.username or "bạn"

    caption = f"""
<blockquote>🚀📖⭐BOT SPAM CALL + SMS⭐📖🚀</blockquote>
<b>Tiện Ích Bot📦🌐</b>

<blockquote expandable>📖
🔰Lệnh tiện ích
» /tt: lấy info TikTok
» /gai, /anime, /vdgai: video/ảnh gái
» /info: Lấy ID
... và nhiều lệnh khác.
</blockquote>
<b>Chúc {username} dùng bot vui vẻ 😘</b>
    """.strip()

    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=video_url,
        caption=caption,
        parse_mode="HTML"
    )

async def handle_capture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != allowed_group_id:
        return

    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng cung cấp URL của trang web.")
        return

    url = context.args[0]
    api_url = f"https://sumiproject.io.vn/cap?link={url}"

    try:
        res = requests.get(api_url)
        data = res.json()

        if 'data' in data and 'screenshotUrl' in data['data']:
            screenshot_url = data['data']['screenshotUrl']
            img = requests.get(screenshot_url)

            if img.status_code == 200:
                with open("screenshot.png", 'wb') as f:
                    f.write(img.content)

                caption = """
┌───⭓ CAP WEBSITE
│» Status : Success🌩️
│» Để sử dụng các lệnh khác
│» Sử dụng /help
└───────────⧕
                """.strip()

                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open("screenshot.png", 'rb'),
                    caption=caption
                )
            else:
                await update.message.reply_text("Không thể lấy ảnh từ API.")
        else:
            await update.message.reply_text("Dữ liệu trả về từ API không hợp lệ.")

    except Exception as e:
        await update.message.reply_text("Đã xảy ra lỗi khi xử lý yêu cầu.")

import requests
from telegram import Update
from telegram.ext import ContextTypes

async def handle_fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Vui lòng sử dụng đúng định dạng: /fb [id hoặc link]")
            return

        fb_id = context.args[0]
        access_token = "EAAD6V7os0gcBO6ZAygwQmTulx9BZABdQM6x4yPN6OvBrCEHy3s8sqd7Lbe0O3x9bd6aHvajNraZCzyYz5VcwnaR6vSXKd0o8f2oOveyNooiZAV8XmxZAqllY9xZBGRNmky87T6zZCvZBZC53vy58Ofptg8mZBRyfsZBkPbERMY6ntgFcH4mUm0FUCbC4I0tKAghjMWhiwZDZD"
        url = f"https://graph.facebook.com/{fb_id}?fields=id,name,picture.width(720).height(720),username,is_verified,created_time,gender,relationship_status,hometown,location,education,work,birthday,about,locale,updated_time,timezone&access_token={access_token}"

        res = requests.get(url)
        data = res.json()

        if "error" in data:
            await update.message.reply_text("Không tìm thấy thông tin cho ID đã nhập.")
            return

        id = data.get("id", "N/A")
        name = data.get("name", "N/A")
        username = data.get("username", "N/A")
        verified = "Có" if data.get("is_verified", False) else "Không"
        created_time = data.get("created_time", "N/A")
        gender = data.get("gender", "N/A")
        relationship_status = data.get("relationship_status", "N/A")
        hometown = data.get("hometown", {}).get("name", "N/A")
        location = data.get("location", {}).get("name", "N/A")
        birthday = data.get("birthday", "N/A")
        locale = data.get("locale", "N/A")
        updated_time = data.get("updated_time", "N/A")
        timezone = data.get("timezone", "N/A")
        work = ", ".join([job.get("employer", {}).get("name", "N/A") for job in data.get("work", [])])
        avatar_url = data.get("picture", {}).get("data", {}).get("url", "N/A")

        message_text = (
            f"<blockquote>╭─────────────⭓\n"
            f"│ 𝗜𝗗: {id}\n"
            f"│ 𝗡𝗮𝗺𝗲: {name}\n"
            f"│ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}\n"
            f"│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱: {verified}\n"
            f"│ 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗧𝗶𝗺𝗲: {created_time}\n"
            f"│ 𝗚𝗲𝗻𝗱𝗲𝗿: {gender}\n"
            f"│ 𝗥𝗲𝗹𝗮𝘁𝗶𝗼𝗻𝘀𝗵𝗶𝗽𝘀: {relationship_status}\n"
            f"│ 𝗛𝗼𝗺𝗲𝘁𝗼𝘄𝗻: {hometown}\n"
            f"│ 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻: {location}\n"
            f"│ 𝗪𝗼𝗿𝗸: {work}\n"
            f"│ 𝗕𝗶𝗿𝘁𝗵𝗱𝗮𝘆: {birthday}\n"
            f"├─────────────⭔\n"
            f"│ 𝗟𝗼𝗰𝗮𝗹𝗲: {locale}\n"
            f"│ 𝗨𝗽𝗱𝗮𝘁𝗲𝗱 𝗧𝗶𝗺𝗲: {updated_time}\n"
            f"│ 𝗧𝗶𝗺𝗲 𝗭𝗼𝗻𝗲: GMT {timezone}\n"
            f"╰─────────────⭓</blockquote>\n"
            f"<a href='{avatar_url}'> ‏ </a>"
        )

        await update.message.reply_text(message_text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"Đã có lỗi xảy ra: {str(e)}")
        

async def reject_other_groups(update: Update, context: ContextTypes.DEFAULT_TYPE): if update.effective_chat.id != allowed_group_id: await update.message.reply_text("Bot chỉ hoạt động trong nhóm này: https://t.me/Spamsmstracuuttvip")

async def paused_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_active:
        return

#====== MAIN APP ======

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL & (~filters.Chat(chat_id=allowed_group_id)), reject_other_groups)) app.add_handler(MessageHandler(filters.ALL, paused_react))

app.add_handler(CommandHandler("info", handle_info)) app.add_handler(CommandHandler("tt", handle_tt)) app.add_handler(CommandHandler("vdgai", handle_video_gai)) app.add_handler(CommandHandler("anime", handle_anime)) app.add_handler(CommandHandler("gai", handle_gai)) app.add_handler(CommandHandler("lenh", handle_welcome)) app.add_handler(CommandHandler("cap", handle_capture)) app.add_handler(CommandHandler("fb", handle_fb))

if name == "main": app.run_polling()

