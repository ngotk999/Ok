from fileinput import filename
import telebot
import os
import subprocess
import time
import datetime
import time
import imghdr
import os,sys,re
import subprocess
import requests
import datetime
import datetime
import sqlite3
import psutil
import hashlib
import random
import json
import logging
import sys
import imghdr
from bs4 import BeautifulSoup
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import urlparse
import threading
from io import BytesIO
import requests
import socket
from time import strftime
from telebot import types
from gtts import gTTS
import tempfile
from telegram.ext import CallbackContext
from telegram import Update, ChatMember
import qrcode
import sqlite3
from telebot import TeleBot
from datetime import date
from datetime import datetime
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify
from datetime import datetime, date
import re
import subprocess
import json
import subprocess
# Configuration Variables
admins = ["ngotk999"]  # Admin username without '@'
name_bot = "𝙎𝙋𝘼𝙈 𝙎𝙈𝙎 𝘾𝘼𝙇𝙇"       # Bot name
zalo = "concac"        # Contact info
web = "hentai.com"  # Website link
boxtele = "Spamsmstracuuttvip"      # Telegram group link
API_URL = "https://api.sumiproject.net/ngl?username={username}&message={message}&amount={amount}"
GPT_API_URL = "https://api.sumiproject.net/gpt4?q={query}"
# Allowed group IDs
allowed_group_ids = [ -1002403107765]  # Must have '-' before chat ID
openai_api_key = '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'
# Bot Token
bot = telebot.TeleBot("7953417537:AAFCyNO6Nj_0VeyE3virc5et7mOdM_bCZj4")  # Token bot
API_TOKEN = 'cặc'  # Thay thế bằng token thật của bạn cho dịch vụ API
# Initialization Message
print("ngotk999 đã được khởi động thành công")
ALLOWED_GROUP_CHAT_ID = -1002403107765
# Admin Usernames and IDs
admin_us = ["ngotk999"]  # List of admin usernames
ADMIN_ID = '6043728545'  # List of admin IDs
app = Flask(__name__)
log_entries = []
# Variables for Bot Functionality
lan = {}
notifi = {}
auto_spam_active = False
last_sms_time = {}
allowed_users = []
processes = []
last_command_time = {}
user_state = {}
conversation_history = {}
sent_messages = []
active_vip_spam_processes = []
# Database Connection
# Dictionary to track user message timestamps
user_messages = {}
vip_folder_path = "./vip"

# Danh sách lưu trạng thái người dùng đã sử dụng /getkey
used_getkey_users = set()  
last_spam_time = {
    "+1234567890": {"last_spam_time": 1627424550, "initiator_name": "John Doe"},
    "+0987654321": {"last_spam_time": 1627426650, "initiator_name": "Jane Smith"}
}

SPAM_MESSAGE = " IB @ngotk999 để vào box !"
SPAM_INTERVAL = 5  # Interval between each spam message in seconds
SPAM_LIMIT = 10  # Limit to prevent indefinite spamming
ALLOWED_GROUP_CHAT_ID = -1002403107765  # Replace with your group's chat ID

# Variables to control spamming and store spammed numbers
is_spamming = False
spam_thread = None
last_spam_time = {}  # Dictionary to store phone numbers with the last spam time
# Mute duration in seconds (4 minutes)
MUTE_DURATION = 240

# Maximum messages allowed within the spam detection window (30 seconds)
MAX_MESSAGES = 15
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
users_keys = {}

# API Configuration
BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None


# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
    now = str(datetime.date.today())
    return now


def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
    '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()

# Kiểm tra và tạo thư mục vip
if not os.path.exists("./vip"):
    os.makedirs("./vip")

GPT_API_URL = 'https://api.openai.com/v1/completions'
headers = {
    'Authorization': f'Bearer {openai_api_key}',  # API Key của OpenAI
    'Content-Type': 'application/json'
}





@bot.message_handler(commands=['add'])
def them(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    parts = message.text.split()
    if len(parts) != 4:
        bot.reply_to(message, 'Vui lòng nhập đầy đủ thông tin: /them <ID> <Ngày Hết Hạn> <Số Ngày>')
        return
    
    idvip = parts[1]
    expiration_date = parts[2]  # Định dạng: DD-MM-YYYY
    expiration_days = parts[3]

    try:
        expiration_date_obj = datetime.strptime(expiration_date, '%d-%m-%Y').date()
    except ValueError:
        bot.reply_to(message, 'Ngày không hợp lệ. Vui lòng sử dụng định dạng DD-MM-YYYY.')
        return
    
    # Lưu vào file
    with open(f"./vip/{idvip}.txt", "w") as fii:
        fii.write(f"{expiration_date}|{expiration_days}")
    
    bot.reply_to(message, f'💥 Thêm thành công {idvip} làm VIP với ngày hết hạn {expiration_date} 💥')





cooldown_dict = {}

@bot.message_handler(commands=['checkspamvip'])
def allspamvip(message):
    vip_dir = "./vip"
    vip_users = []
    
    # Check if the VIP directory exists
    if not os.path.exists(vip_dir):
        bot.reply_to(message, "Không có VIP nào được đăng ký.")
        return
    
    # Loop through each VIP file
    for vip_file in os.listdir(vip_dir):
        user_id = os.path.splitext(vip_file)[0]
        vip_file_path = os.path.join(vip_dir, vip_file)
        
        try:
            with open(vip_file_path) as fo:
                data = fo.read().strip().split("|")
            
            expiration_date_str = data[0]
            expiration_date_obj = datetime.strptime(expiration_date_str, '%d-%m-%Y').date()
            remaining_days = (expiration_date_obj - date.today()).days
            
            # Check if VIP is active
            if remaining_days >= 0:
                vip_users.append(f"User ID: {user_id}\n+ Ngày hết hạn: {expiration_date_str}\n+ Số ngày còn lại: {remaining_days} ngày\n")
            else:
                os.remove(vip_file_path)  # Remove expired VIP file
        except (ValueError, IndexError, FileNotFoundError):
            bot.reply_to(message, f"Thông tin VIP của {user_id} không hợp lệ. Vui lòng kiểm tra lại.")
            continue

    # Compile and send VIP list
    if vip_users:
        vip_list = "\n\n".join(vip_users)
        bot.reply_to(message, f"✨ Danh sách VIP hiện tại ✨\n\n{vip_list}")
    else:
        bot.reply_to(message, "Không có VIP nào được đăng ký hoặc tất cả đã hết hạn.")
last_spam_time = {}
@bot.message_handler(commands=['spamvip'])
def spamvip(message):
    # Check if the message is in the allowed group chat
    

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    # Check if the user is registered as VIP
    vip_file_path = f"./vip/{user_id}.txt"
    if not os.path.exists(vip_file_path):
        bot.reply_to(message, 'Bạn chưa đăng ký VIP. Vui lòng liên hệ admin.')
        return

    try:
        # Read VIP info (expiration date and days)
        with open(vip_file_path) as fo:
            data = fo.read().split("|")
        
        expiration_date_str = data[0]  # Expiration date in DD-MM-YYYY
        expiration_days = int(data[1])  # Number of days
        expiration_date_obj = datetime.strptime(expiration_date_str, '%d-%m-%Y').date()
    except (ValueError, IndexError):
        bot.reply_to(message, 'Thông tin VIP không hợp lệ. Vui lòng liên hệ admin.')
        return

    # Check if VIP access has expired
    today = date.today()
    if today > expiration_date_obj:
        bot.reply_to(message, 'Key VIP đã hết hạn. Vui lòng liên hệ admin.')
        os.remove(vip_file_path)  # Remove expired VIP file
        return

    # Ensure phone number argument is provided
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Vui lòng nhập số điện thoại.')
        return

    phone_number = message.text.split()[1]
    
    # Validate phone number format
    if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'Số điện thoại không hợp lệ!')
        return

    # Paths to external scripts
    script_files = ["text1.py", "text2.py", "text3.py", "text4.py", "text5.py", "text6.py", "text7.py", "text8.py", "text9.py", "text10.py"]
    
    # Cooldown mechanism (120 seconds per user)
    current_time = time.time()
    if phone_number in last_spam_time:
        time_since_last_spam = current_time - last_spam_time[phone_number]
        if time_since_last_spam < 600:
            remaining_time = int(600 - time_since_last_spam)
            bot.reply_to(message, f'Số điện thoại {phone_number} đã được spam. Vui lòng đợi {remaining_time} giây trước khi thử lại.')
            return
    last_spam_time[phone_number] = current_time
    # Update cooldown dictionary with 120-second wait
    cooldown_dict[username] = {'vip': current_time}

    # Execute external scripts concurrently and count them
    processes = []
    count = 0
    for script_file in script_files:
        script_path = os.path.join(os.getcwd(), script_file)
        process = subprocess.Popen(["python", script_path, phone_number, "50"])
        processes.append(process)
        count += 1

    # Print statement to log information
    print(f"user vip User ID: {user_id}, Name: {full_name}, Phone: {phone_number}, Count: 50 ")



    # Send confirmation to user with full name and phone number
    
    
    xinchao = f"""<blockquote> cái địt mẹ mày thằng {full_name}
    Attack Sent by : @{username}
    Gửi yêu cầu tấn công thành công 🚀
     Số tấn công 📱: [ {phone_number} ]
     Số lượt Tấn công 📱: [ 33 Lần ]
     Plan Của Bạn : [ VIP ] 
     Tên người dùng 👤: [ {full_name} ]
     </blockquote>
     """
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
      types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),        
    )

    video_url = "https://files.catbox.moe/xbgx14.mp4"
    bot.send_video(message.chat.id, video_url, caption=xinchao, parse_mode='HTML', reply_markup=keyboard)

    # Gửi tin nhắn "loading"
    sent_message = bot.reply_to(message, "Đang xử lý...")

    # Chuỗi hiệu ứng "Loading"
    
    loading_frames = [
        "Buy GÌ Cứ Ib @ngotk999 dcu ",
        "cái địt mẹ mày  ...",        
    ]
    

    # Hiệu ứng "Loading"
    for _ in range(1):  # Lặp 3 lần hiệu ứng
        for frame in loading_frames:
            bot.edit_message_text(frame, chat_id=message.chat.id, message_id=sent_message.message_id)
            time.sleep(0.2)

    # Cập nhật trạng thái spam
    bot.edit_message_text(f"\n\n[ {full_name} ] Bắt Đầu Spam  {phone_number}  ", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(1)  # Chờ trước khi xóa

    # Xóa tin nhắn cũ
    bot.delete_message(message.chat.id, message.message_id)  # Xóa tin nhắn lệnh gốc
    bot.delete_message(message.chat.id, sent_message.message_id)  # Xóa tin nhắn "loading"



@bot.message_handler(commands=['smsvip'])
def smsvip(message):
    # Check if the message is in the allowed group chat
    

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    # Check if the user is registered as VIP
    vip_file_path = f"./vip/{user_id}.txt"
    if not os.path.exists(vip_file_path):
        bot.reply_to(message, 'Bạn chưa đăng ký VIP. Vui lòng liên hệ admin @ngotk999.')
        return

    try:
        # Read VIP info (expiration date and days)
        with open(vip_file_path) as fo:
            data = fo.read().split("|")
        
        expiration_date_str = data[0]  # Expiration date in DD-MM-YYYY
        expiration_days = int(data[1])  # Number of days
        expiration_date_obj = datetime.strptime(expiration_date_str, '%d-%m-%Y').date()
    except (ValueError, IndexError):
        bot.reply_to(message, 'Thông tin VIP không hợp lệ. Vui lòng liên hệ admin.')
        return

    # Check if VIP access has expired
    today = date.today()
    if today > expiration_date_obj:
        bot.reply_to(message, 'Key VIP đã hết hạn. Vui lòng liên hệ admin.')
        os.remove(vip_file_path)  # Remove expired VIP file
        return

    # Ensure phone number argument is provided
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Vui lòng nhập số điện thoại.')
        return

    phone = message.text.split()[1]
    
    # Validate phone number format
    if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone):
        bot.reply_to(message, 'Số điện thoại không hợp lệ!')
        return

    # Paths to external scripts
    script_files = ["text1.py"]
    
    # Cooldown mechanism (120 seconds per user)
    current_time = time.time()
    if phone in last_spam_time:
        time_since_last_spam = current_time - last_spam_time[phone]
        if time_since_last_spam < 600:
            remaining_time = int(600 - time_since_last_spam)
            bot.reply_to(message, f'Số điện thoại {phone} đã được spam. Vui lòng đợi {remaining_time} giây trước khi thử lại.')
            return
    last_spam_time[phone] = current_time
    # Update cooldown dictionary with 120-second wait
    cooldown_dict[username] = {'vip': current_time}

    # Execute external scripts concurrently and count them
    processes = []
    spam_count = 0
    for script_file in script_files:
        script_path = os.path.join(os.getcwd(), script_file)
        process = subprocess.Popen(["python", script_path, phone, "5"])
        processes.append(process)
        spam_count += 1

    # Print statement to log information
    print(f"user smsvip User ID: {user_id}, Name: {full_name}, Phone: {phone}, spam_count: 500 ")



    # Send confirmation to user with full name and phone number
    
    
    xinchao = f"""<blockquote> cái địt mẹ mày thằng {full_name}
    Attack Sent by : @{username}
    Gửi yêu cầu tấn công thành công 🚀
    Số tấn công 📱: [ {phone} ]
    Số lần spam📱: [  100 ]
    Plan Của Bạn : [ VIP ] 
    Tên người dùng 👤: [ {full_name} ]
     </blockquote>
     """
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
      types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),        
    )

    video_url = "https://files.catbox.moe/xbgx14.mp4"
    bot.send_video(message.chat.id, video_url, caption=xinchao, parse_mode='HTML', reply_markup=keyboard)

    # Gửi tin nhắn "loading"
    sent_message = bot.reply_to(message, "Đang xử lý...")

    # Chuỗi hiệu ứng "Loading"
    
    loading_frames = [
        "Buy GÌ Cứ Ib @ngotk999 dcu ",
        "cái địt mẹ mày  ...",        
    ]
    

    # Hiệu ứng "Loading"
    for _ in range(1):  # Lặp 3 lần hiệu ứng
        for frame in loading_frames:
            bot.edit_message_text(frame, chat_id=message.chat.id, message_id=sent_message.message_id)
            time.sleep(0.2)

    # Cập nhật trạng thái spam
    bot.edit_message_text(f"\n\n[ {full_name} ] Bắt Đầu Spam  {phone}  ", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(1)  # Chờ trước khi xóa

    # Xóa tin nhắn cũ
    bot.delete_message(message.chat.id, message.message_id)  # Xóa tin nhắn lệnh gốc
    bot.delete_message(message.chat.id, sent_message.message_id)  # Xóa tin nhắn "loading"





def save_card_info(serial, pin, amount, carrier, full_name, username):
    with open('napthe.txt', 'a', encoding='utf-8') as file:  # Mở tệp với encoding='utf-8'
        file.write(f"Seri: {serial}, Mã thẻ: {pin}, Mệnh giá: {amount}, Nhà mạng: {carrier}, Người dùng: {full_name} (@{username})\n")

# Hàm gửi thông báo đến admin về giao dịch nạp thẻ
def notify_admin_about_card(serial, pin, amount, carrier, full_name, username):
    notification = f"""
    🏷️ Thông báo Nạp Thẻ:

    💳 Seri: {serial}
    🔑 Mã thẻ: {pin}
    💵 Mệnh giá: {amount} VND
    📱 Nhà mạng: {carrier}
    📝 Người dùng: {full_name} (@{username})
    """
    try:
        bot.send_message(ADMIN_ID, notification)
        print("Thông báo đã được gửi đến admin.")
    except Exception as e:
        print(f"Lỗi khi gửi thông báo đến admin: {e}")

# Lệnh yêu cầu thông tin thẻ từ người dùng
@bot.message_handler(commands=['napthe'])
def request_card_info(message):
    # Yêu cầu người dùng nhập seri thẻ
    msg = bot.reply_to(message, "Vui lòng nhập Seri thẻ:")
    bot.register_next_step_handler(msg, process_card_serial)

# Xử lý thông tin thẻ sau khi người dùng nhập Seri
def process_card_serial(message):
    serial = message.text.strip()

    # Yêu cầu người dùng nhập mã thẻ
    msg = bot.reply_to(message, "Vui lòng nhập mã thẻ:")
    bot.register_next_step_handler(msg, process_card_pin, serial)

# Xử lý mã thẻ
def process_card_pin(message, serial):
    pin = message.text.strip()

    # Yêu cầu người dùng nhập mệnh giá thẻ
    msg = bot.reply_to(message, "Vui lòng nhập mệnh giá thẻ (VND):")
    bot.register_next_step_handler(msg, process_card_amount, serial, pin)

# Xử lý mệnh giá thẻ
def process_card_amount(message, serial, pin):
    amount = message.text.strip()

    # Yêu cầu người dùng nhập nhà mạng
    msg = bot.reply_to(message, "Vui lòng nhập nhà mạng (Viettel, Mobifone, Vinaphone, vv):")
    bot.register_next_step_handler(msg, process_card_carrier, serial, pin, amount)

# Xử lý nhà mạng
def process_card_carrier(message, serial, pin, amount):
    carrier = message.text.strip()

    # Lưu thông tin thẻ vào file
    save_card_info(serial, pin, amount, carrier, message.from_user.full_name, message.from_user.username)

    # Thông báo cho người dùng rằng giao dịch đã được ghi nhận
    bot.reply_to(message, "Admin Đang Check Mã Thẻ Vui Lòng Chờ 1 - 2 PHÚT !")

    # Gửi thông báo cho admin về giao dịch nạp thẻ
    notify_admin_about_card(serial, pin, amount, carrier, message.from_user.full_name, message.from_user.username)

# Chạy bot







@bot.message_handler(commands=['checkuserspam'])
def checkuserspam(message):
    # Ensure an argument (phone number or VIP username) is provided
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Vui lòng nhập số điện thoại hoặc tên đăng nhập VIP để kiểm tra.')
        return

    identifier = message.text.split()[1]

    # Check if identifier is a phone number or a username
    if identifier.isdigit():
        # Treat identifier as a phone number
        phone_number = identifier
        if phone_number in last_spam_time:
            # Calculate time since last spam for the phone number
            last_time = last_spam_time[phone_number]
            time_since_last_spam = time.time() - last_time
            remaining_cooldown = max(0, int(220 - time_since_last_spam))

            if remaining_cooldown > 0:
                bot.reply_to(message, f"Số điện thoại {phone_number} đã được spam gần đây. Vui lòng đợi {remaining_cooldown} giây trước khi spam lại.")
            else:
                bot.reply_to(message, f"Số điện thoại {phone_number} có thể được spam lại.")
        else:
            bot.reply_to(message, f"Số điện thoại {phone_number} chưa bị spam gần đây và có thể được spam.")

    else:
        # Treat identifier as a VIP username
        username = identifier
        if username in cooldown_dict and 'vip' in cooldown_dict[username]:
            last_time = cooldown_dict[username]['vip']
            time_since_last_spam = time.time() - last_time
            remaining_cooldown = max(0, int(220 - time_since_last_spam))

            if remaining_cooldown > 0:
                bot.reply_to(message, f"Người dùng VIP @{username} đã sử dụng lệnh spamvip gần đây. Vui lòng đợi {remaining_cooldown} giây trước khi dùng lại.")
            else:
                bot.reply_to(message, f"Người dùng VIP @{username} có thể sử dụng lệnh spamvip.")
        else:
            bot.reply_to(message, f"Người dùng VIP @{username} chưa sử dụng lệnh spamvip gần đây và có thể sử dụng.")

@bot.message_handler(commands=['test'])
def test(message):
    # Check if the message is in the allowed group chat
    

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    # Check if the user is registered as VIP
    vip_file_path = f"./vip/{user_id}.txt"
    if not os.path.exists(vip_file_path):
        bot.reply_to(message, 'Bạn chưa đăng ký VIP. Vui lòng liên hệ admin.')
        return

    try:
        # Read VIP info (expiration date and days)
        with open(vip_file_path) as fo:
            data = fo.read().split("|")
        
        expiration_date_str = data[0]  # Expiration date in DD-MM-YYYY
        expiration_days = int(data[1])  # Number of days
        expiration_date_obj = datetime.strptime(expiration_date_str, '%d-%m-%Y').date()
    except (ValueError, IndexError):
        bot.reply_to(message, 'Thông tin VIP không hợp lệ. Vui lòng liên hệ admin.')
        return

    # Check if VIP access has expired
    today = date.today()
    if today > expiration_date_obj:
        bot.reply_to(message, 'Key VIP đã hết hạn. Vui lòng liên hệ admin.')
        os.remove(vip_file_path)  # Remove expired VIP file
        return

    # Ensure phone number argument is provided
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Vui lòng nhập số điện thoại.')
        return

    phone_number = message.text.split()[1]
    
    # Validate phone number format
    if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'Số điện thoại không hợp lệ!')
        return

    # Paths to external scripts
    script_files = ["text1.py", "text2.py", "text3.py", "text4.py", "text5.py", "text6.py", "text7.py", "text8.py", "text9.py", "text10.py"]
    
    # Cooldown mechanism (120 seconds per user)
    current_time = time.time()
    if phone_number in last_spam_time:
        time_since_last_spam = current_time - last_spam_time[phone_number]
        if time_since_last_spam < 120:
            remaining_time = int(120 - time_since_last_spam)
            bot.reply_to(message, f'Số điện thoại {phone_number} đã được spam. Vui lòng đợi {remaining_time} giây trước khi thử lại.')
            return
    last_spam_time[phone_number] = current_time
    # Update cooldown dictionary with 120-second wait
    cooldown_dict[username] = {'vip': current_time}

    # Execute external scripts concurrently and count them
    processes = []
    count = 0
    for script_file in script_files:
        script_path = os.path.join(os.getcwd(), script_file)
        process = subprocess.Popen(["python", script_path, phone_number, "5"])
        processes.append(process)
        count += 1

    # Print statement to log information
    print(f"/test User ID: {user_id}, Name: {full_name}, Phone: {phone_number}, Count: 5 ")



    # Send confirmation to user with full name and phone number
    
    
    response = (
    f" Attack sent  \n"
    f"🚀 Gửi yêu cầu tấn công thành công 🚀\n"
    f"+ Số tấn công 📱: [ {phone_number} ]\n"
    f"+ Số lượt Tấn công 📱: [ 5 Lần ]\n"
    f"+ Tên người dùng 👤: {full_name} (@{username})"
)
    sent_message = bot.reply_to(message, response)   
# Send the reply
    bot.reply_to(message,response)
    # Short delay to ensure the bot has sent the reply
    # Wait for a moment before the next part of the "shattering" effect
    
    bot.edit_message_text(f"\n\n 3 ", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    # Another effect stage (disintegration)
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading .", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(1)
    
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading .", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading .", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(0.2)

    bot.edit_message_text(f"\n\n[ {full_name} ] Bắt Đầu Spam  {phone_number}  ", chat_id=message.chat.id, message_id=sent_message.message_id)
    # Another effect stage (disintegration)
    time.sleep(1)
    bot.delete_message(message.chat.id, message.message_id)  # Delete the original message
    bot.delete_message(sent_message.chat.id, sent_message.message_id)


@bot.message_handler(commands=['attack'])
def test(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    # Check VIP status
    vip_file_path = f"./vip/{user_id}.txt"
    if not os.path.exists(vip_file_path):
        bot.reply_to(message, 'Bạn chưa đăng ký VIP. Vui lòng liên hệ admin.')
        return

    try:
        # Read VIP information
        with open(vip_file_path) as fo:
            data = fo.read().split("|")
        
        expiration_date_str = data[0]  # Expiration date in DD-MM-YYYY
        expiration_date_obj = datetime.strptime(expiration_date_str, '%d-%m-%Y').date()
    except (ValueError, IndexError):
        bot.reply_to(message, 'Thông tin VIP không hợp lệ. Vui lòng liên hệ admin.')
        return

    # Check if VIP access has expired
    today = date.today()
    if today > expiration_date_obj:
        bot.reply_to(message, 'Key VIP đã hết hạn. Vui lòng liên hệ admin.')
        os.remove(vip_file_path)  # Remove expired VIP file
        return

    # Ensure necessary arguments are provided
    args = message.text.split()
    if len(args) < 5:  # Expecting: /attack host time port methods
        bot.reply_to(
            message, 
            "Vui lòng nhập đủ thông tin: /attack <host> <time> <port> <method>\n"
            "method = [layer7 .tls-kill .browser | layer4 .ovh-killer]"
        )
        return

    host = args[1]
    time = args[2]
    port = args[3]
    methods = args[4]

    try:
        # API request
        api_url = f"http://api.ventox.id.vn/api/attack"
        params = {
            "username": "ventox",
            "key": "ventox",
            "host": host,
            "time": time,
            "port": port,
            "method": methods
        }
        response = requests.get(api_url, params=params)

        # Handle API response
        if response.status_code == 200:
            message_text = (
                f"🚀 **Attack Sent!** 🚀\n"
                f"Host: [ {host} ]\n"
                f"Port: [ {port} ]\n"
                f"Time: [ {time} ]\n"
                f"Method: [ {methods} ]\n"
                f"Requested by: {full_name} (@{username})"
            )
        else:
            message_text = f"Lỗi API: {response.status_code} - {response.text}"

    except Exception as e:
        message_text = f"Không thể gửi yêu cầu API: {str(e)}"

    # Send the result to the user
    bot.reply_to(message, message_text, parse_mode="Markdown")





@bot.message_handler(commands=['stopspamvip'])
def stopspamvip(message):
    user_id = message.from_user.id

    # Kiểm tra quyền truy cập của người dùng
    if user_id != ADMIN_ID:  # Ensure we're using ADMIN_ID correctly
        vip_file_path = f"./vip/{user_id}.txt"
        if not os.path.exists(vip_file_path):
            bot.reply_to(message, "❌ Bạn không có quyền dừng spam VIP.")
            return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "⚠️ Vui lòng cung cấp số điện thoại để dừng spam VIP.")
        return

    phone_number = message.text.split()[1]

    # Kiểm tra xem có tiến trình spam nào cho số điện thoại này không
    if phone_number in active_vip_spam_processes:
        if user_id == ADMIN_ID or user_id == message.from_user.id:
            # Attempt to stop all processes associated with the phone number
            try:
                for process in active_vip_spam_processes[phone_number]:
                    process.terminate()  # Dừng tiến trình
                    process.wait()  # Đảm bảo tiến trình đã kết thúc
                    bot.reply_to(message, f"✅ Đã dừng spam VIP cho số điện thoại {phone_number}.")
                
                # Xóa số điện thoại khỏi danh sách sau khi dừng spam
                del active_vip_spam_processes[phone_number]
            except Exception as e:
                bot.reply_to(message, f"❌ Lỗi khi dừng spam: {str(e)}")
        else:
            bot.reply_to(message, "❌ Bạn không có quyền dừng spam này.")
    else:
        bot.reply_to(message, f"❌ Không tìm thấy tiến trình spam VIP nào cho số điện thoại {phone_number}.")


@bot.message_handler(commands=['listspammed'])
def list_spammed(message):
    if not last_spam_time:
        bot.reply_to(message, "There are currently no spammed numbers.")
        return

    response = "Recently spammed numbers:\n\n"
    current_time = time.time()

    for phone_number, last_time in last_spam_time.items():
        time_since_last_spam = int(current_time - last_time)
        remaining_cooldown = max(0, SPAM_INTERVAL - time_since_last_spam)  # Adjust cooldown if needed

        response += (
            f" _______________________________\n"
            f"  + Số điện thoại : {phone_number}\n"
            f"  + Time spam : {time_since_last_spam} Giây Trước\n"
            f"  + Time còn lại : {remaining_cooldown} Giây \n"
            f" _______________________________\n\n"
        )

    bot.reply_to(message, response)



@bot.message_handler(commands=['huyvip'])
def remove_vip(message):
    admin_id = message.from_user.id
    if str(admin_id) != ADMIN_ID:  # So sánh với ADMIN_ID dưới dạng chuỗi
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Xin cung cấp ID người dùng để huỷ quyền VIP.')
        return

    user_id = int(message.text.split()[1])
    # Xóa VIP trong file
    vip_file_path = f"./vip/{user_id}.txt"
    if os.path.exists(vip_file_path):
        os.remove(vip_file_path)
        bot.reply_to(message, f'Người dùng {user_id} đã bị huỷ quyền VIP thành công.')
    else:
        bot.reply_to(message, f'Người dùng {user_id} không phải là VIP.')

start_time = time.time()  # Ghi lại thời gian bắt đầu

def get_elapsed_time():
    elapsed_time = time.time() - start_time  # Tính thời gian đã trôi qua
    return elapsed_time

load_users_from_database()
def is_key_approved(chat_id, key):
    if chat_id in users_keys:
        user_key, timestamp = users_keys[chat_id]
        if user_key == key:
            current_time = datetime.datetime.now()
            if current_time - timestamp <= datetime.timedelta(hours=2):
                return True
            else:
                del users_keys[chat_id]
    return False
def escape_markdown(text):
    """Thoát các ký tự đặc biệt để sử dụng trong chế độ MarkdownV2"""
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    username = message.from_user.username
    xinchao = f"""<blockquote> 🚀📖⭐BOT SPAM CALL + SMS⭐📖🚀 </blockquote>
<b>[⭐] Xin chào @{username}</b> 
<blockquote expandable>📖 18 câu lệnh dành cho người dùng
⭐ Lệnh khởi đầu
» /start: Lệnh khởi đầu 
» /help: Lệnh trợ giúp 
⚔️ Lệnh Spam
» /getkey: Để lấy key ngày 
» /key: Để nhập key ngày
» /spam: Spam 20 lần  
» /ngl: Spam ngl
» /stop_spam: Dừng spam sđt </blockquote>"
<blockquote expandable>🔰Khi taọ key mới dùng được
» /enkey: khi có key đc tạo bởi admin
» /taokey: tạo key chỉ có admin  
» /spams: spam có call </blockquote>
️<blockquote expandable>🏆 Lệnh cho thành viên VIP: /vip </blockquote>"
<blockquote expandable>🔰Lệnh tiện ích
» /napthe: Nạp thẻ Tới Admin 
» /bank: bank tiền admin  
» /admin: Thông tin admin 
» /checkfb: Thông tin Fb
» /voice: Để đổi văn bản thành giọng nói
» /info: Để lấy id người của bản thân  
» /checkip: Để check thông tin ip 
» /vi_pham: Để check vi phạm cho biển số 
» /avtfb: getavtfb xuyên khiêng
» /tiktok: Để lấy thông tin video 
» /qr: tạo mã qr 
» /adm: lệnh cho admin
» /html: lấy html web </blockquote>
"""

    # Tạo các nút nằm ngang
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
      types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),
        types.InlineKeyboardButton("🤖 Bot", url="https://t.me/KLTOOLBOT")
    )

    video_url = "https://files.catbox.moe/xbgx14.mp4"
    bot.send_video(message.chat.id, video_url, caption=xinchao, parse_mode='HTML', reply_markup=keyboard)
# Hàm lấy Facebook ID từ API
def get_facebook_id(link: str) -> str:
    api_url = f"https://api.sumiproject.net/facebook/uid?link={link}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('id', 'Không tìm thấy ID')
    else:
        return f"Lỗi API: {response.status_code}"
@bot.message_handler(commands=['vip'])
def send_welcome(message):
    username = message.from_user.username
    lenhvip = f"""<blockquote> 🚀📖⭐BOT SPAM CALL + SMS⭐📖🚀 </blockquote>
<b>[⭐] Xin chào @{username}</b> 
<blockquote expandable>📖 Tất Cả câu lệnh dành cho ADM
️🥈Lệnh Cho VIP
» /spamvip: Call Spam API Múp
» /smsvip :  Sms Spam API Múp
» /checkuserspam : Check của bạn
» /listspammed : danh sách spam</blockquote>
<blockquote expandable>📖 Tất Cả SMS Vip
️🥈Lệnh Cho Vip Basic
» /smsvip: Call Spam API Lt</blockquote>
<blockquote expandable>📖 Tất Cả Basic
️🥈Lệnh Cho Vip Basic
» /spambasic: Call Spam API Lt</blockquote>
<blockquote expandable>🥈Lệnh Cho VIP Khi Vip Test Khách
» /test : Spam Vip Test Khách
» /attack : ddos web end ip layer 4
» @ngotk999
</blockquote>"""
        
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
        types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),
        types.InlineKeyboardButton("🤖 Bot", url="https://t.me/KLTOOLBOT")
    )

    video_url = "https://files.catbox.moe/yaztwg.mp4"
    bot.send_video(message.chat.id, video_url, caption=lenhvip, parse_mode='HTML', reply_markup=keyboard)


@bot.message_handler(commands=['adm'])
def send_welcome(message):
    username = message.from_user.username
    lenhadmin = f"""<blockquote> 🚀📖⭐BOT SPAM CALL + SMS⭐📖🚀 </blockquote>
<b>[⭐] Xin chào @{username}</b> 
<blockquote expandable>📖 Tất Cả câu lệnh dành cho ADM
🔰Lệnh Cho Admin
» /cpu: Để xem cấu hình
» /restart: Để khởi động lại bot
» /all: Để thông báo cho cả nhóm
» /huyvip: Để hủy vip bằng id
» /im: Để khóa mõm 
» /unim: Để mở khóa mõm
» /add: Để thêm người dùng vào vip
» /huyvip: Để hủy vip
» /lock: Để khóa chat
» /unlock: Để mở chat
» /ban: Để kick người dùng</blockquote>"""
        
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
        types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),
        types.InlineKeyboardButton("🤖 Bot", url="https://t.me/KLTOOLBOT")
    )

    video_url = "https://files.catbox.moe/yaztwg.mp4"
    bot.send_video(message.chat.id, video_url, caption=lenhadmin, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(commands=['napvip'])
def send_welcome(message):
    user_id = message.from_user.id
    with open('id', 'r') as file:
        if str(message.chat.id) not in file.read():
            with open('id', 'a') as file:
                file.write(str(message.chat.id) + '\n')
    username = escape_markdown(message.from_user.username)
    xinchao = f"""     ⭓ {escape_markdown(name_bot)} ⭓
» Xin chào @{username}
» /bank: Bank tiền
"""
    video_url = "https://files.catbox.moe/yaztwg.mp4"
    bot.send_video(message.chat.id, video_url, caption=xinchao, parse_mode='MarkdownV2')
@bot.message_handler(commands=['bank'])
def handle_bank(message):
    markup = types.InlineKeyboardMarkup()
    btn_momo = types.InlineKeyboardButton(text='Momo', callback_data='momo')
    btn_mbbank = types.InlineKeyboardButton(text='mbbank', callback_data='mbbank')

    markup.add(btn_momo)
    bot.reply_to(message, "Vui Lòng Chọn Bank:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['momo'])
def handle_bank_selection(call):
    user_id = call.from_user.id
    if call.data == 'mbbank':
        qr_code_url = f""
        caption = f"""
> ┌────⭓ BIDV ⭓────
> ├ Ngân Hàng: 𝙈𝘽 𝘽𝘼𝙉𝙆
> ├ STK: 9704229201122741793
> ├ Tên: 𝙉𝙜𝙪𝙮𝙚𝙣 𝙩𝙝𝙞 𝙣𝙜𝙤𝙘 𝙮𝙚𝙣 
> ├ ND: 𝙣𝙖𝙥𝙫𝙞𝙥_{user_id}
> ├ Số Tiền: 20.000 𝙑𝙉𝘿
> └───────[✓]───────

Lưu Ý:
    + Khi Bank Nhớ Nhập Đúng Nội Dung Chuyển Tiền.
    + Khi Bank Xong Vui Lòng Liên Hệ @ngotk999 Để Add Vip.
"""
        # Escape the caption
        caption = escape_markdown(caption)

        bot.send_photo(call.message.chat.id, qr_code_url, caption=caption, parse_mode='MarkdownV2')
    elif call.data == 'momo':
        momo = f"""
> ┌────⭓ Mbbank ⭓────
> ├ Ngân Hàng: Momo
> ├ STK: 9704229201122741793
> ├ Tên: 𝙉𝙜𝙪𝙮𝙚𝙣 𝙩𝙝𝙞 𝙣𝙜𝙤𝙘 𝙮𝙚𝙣 
> ├ ND: 𝙣𝙖𝙥𝙫𝙞𝙥_{user_id}
> ├ Số Tiền: 20.000 VNĐ
> └───────[✓]───────

Lưu Ý:
    + Khi Bank Nhớ Nhập Đúng Nội Dung Chuyển Tiền.
    + Khi Bank Xong Vui Lòng Liên Hệ @ngotk999 Để Add Vip.
"""
        # Escape the momo message
        momo = escape_markdown(momo)

        bot.reply_to(call.message, momo, parse_mode='MarkdownV2')
@bot.message_handler(commands=['admin'])
def send_admin_info(message):
    username = message.from_user.username
    admin_info = f'''
    ⭓ {escape_markdown(name_bot)} ⭓
    » Xin chào @{escape_markdown(username)}
    » Admin: [Click](@{admins})
    » Zalo: {escape_markdown(zalo)}
    » Website: {escape_markdown(web)}
    » Telegram: @{escape_markdown(admins)}
    » Lưu Ý: Spam Liên
       Tục Lệnh Ăn Ban
       Đừng Kêu Mở 
    '''
    video_url = "https://files.catbox.moe/5l74tr.mp4"
    bot.send_video(message.chat.id, video_url, caption=admin_info, parse_mode='MarkdownV2')

@bot.message_handler(commands=['cpu'])
def check_system_info(message):
    admin_id = message.from_user.id
    if str(admin_id) != ADMIN_ID:  # So sánh với ADMIN_ID dưới dạng chuỗi
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    message_text = f"🖥 Thông Tin Pc 🖥\n\n" \
                   f"🇻🇳 Admin: Tấn kiệt Dzz 🇻🇳\n\n" \
                   f"📊 Cpu: {cpu_percent}%\n" \
                   f"🧠 Memory: {memory_percent}%"
    bot.reply_to(message, message_text)

@bot.message_handler(commands=['restart'])
def restart(message):
    admin_id = message.from_user.id
    if str(admin_id) != ADMIN_ID:  # So sánh với ADMIN_ID dưới dạng chuỗi
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    bot.reply_to(message, '🚀 Bot sẽ được khởi động lại trong giây lát... 🚀')
    time.sleep(10)
    python = sys.executable
    os.execl(python, python, *sys.argv)


is_bot_active = True
import os
import subprocess
import time

cooldown_dict = {}
processes = []



@bot.message_handler(commands=['all'])
def notify_all_members(message):
    admin_id = message.from_user.id
    if str(admin_id) != ADMIN_ID:  # Check if the sender is the admin
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    try:
        # Get the list of administrators
        admins = bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]

        # Create the notification message for admins
        notification = "<b>📢 Thông báo từ admin:</b>\n"

        # Tagging all admins
        for admin in admins:
            notification += f"@{admin.user.username} " if admin.user.username else ""

        # Send notification to all admins
        bot.send_message(message.chat.id, notification, parse_mode='HTML')

        # Send a message to all group members (excluding the bot itself)
        members = bot.get_chat_members(message.chat.id)  # Get list of all members
        for member in members:
            if member.user.is_bot:  # Skip bots
                continue

            # Send a notification to each user
            bot.send_message(
                member.user.id,
                "📢 Đây là thông báo từ admin!\n" + notification,
                parse_mode='HTML'
            )

    except Exception as e:
        bot.reply_to(message, '<blockquote>Không thể gửi thông báo. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>', parse_mode='HTML')

@bot.message_handler(commands=['gemini'])
def start_gemini_conversation(message):
    user_id = message.from_user.id

    # Kiểm tra quyền sử dụng lệnh
    if message.from_user.username not in admin_us:
        bot.reply_to(message, "Bạn Không Có Quyền Sử Dụng Lệnh Này")
        return

    # Lấy nội dung sau lệnh /gemini
    input_text = message.text[8:].strip()

    if not input_text:
        bot.reply_to(message, "Vui lòng cung cấp đầu vào.")
        return
    # Khởi tạo lịch sử cuộc trò chuyện cho người dùng
    conversation_history[user_id] = [{"role": "user", "content": input_text}]
    # Gọi API và trả lời người dùng
    send_to_gemini_api(message, user_id, input_text)

# Xử lý lệnh /getid
@bot.message_handler(commands=['getid'])
def send_facebook_id(message):
    waiting_message = bot.reply_to(message, '🔍')
    try:
        # Tách link từ tin nhắn của người dùng
        link = message.text.split()[1]
        facebook_id = get_facebook_id(link)
        bot.reply_to(message, f"<b>ID cho link </b>: <code>{facebook_id}</code>", parse_mode='html')
        bot.delete_message(message.chat.id, waiting_message.message_id)
    except IndexError:
        bot.reply_to(message, "Vui lòng cung cấp link Facebook hợp lệ sau lệnh /getid.")
        bot.delete_message(message.chat.id, waiting_message.message_id)
@bot.message_handler(commands=['avtfb'])
def get_facebook_avatar(message):
    user_id = message.from_user.id

    # Check command format
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Vui lòng nhập đúng định dạng\nExample: /avtfb [link hoặc id]')
        return
    
    # Gửi tin nhắn chờ xử lý
    waiting_message = bot.reply_to(message, '🔍')

    # Get parameter from the message
    parameter = message.text.split()[1]

    # Determine if it's a Facebook ID or a link
    if parameter.isdigit():  # If it's a Facebook ID
        facebook_id = parameter
    else:  # If it's a Facebook link
        if 'facebook.com' not in parameter:
            bot.edit_message_text('Liên kết không phải từ Facebook', message.chat.id, waiting_message.message_id)
            return
        
        # Use the API to get the Facebook ID from the URL
        api_url = f"https://api.sumiproject.net/facebook/uid?link={parameter}"
        try:
            api_response = requests.get(api_url)
            api_response.raise_for_status()
            json_response = api_response.json()
            
            if 'id' in json_response:
                facebook_id = json_response['id']
            else:
                bot.edit_message_text('Không thể lấy ID từ liên kết Facebook. Vui lòng thử lại với một liên kết khác.', message.chat.id, waiting_message.message_id)
                return
            
        except requests.RequestException as e:
            bot.edit_message_text(f'Có lỗi xảy ra khi truy cập API: {e}', message.chat.id, waiting_message.message_id)
            return
        except Exception as e:
            bot.edit_message_text(f'Có lỗi xảy ra: {e}', message.chat.id, waiting_message.message_id)
            return

    # Use the provided Facebook URL for the profile picture
    graph_url = f"https://graph.facebook.com/{facebook_id}/picture?width=1500&height=1500&access_token=2712477385668128%7Cb429aeb53369951d411e1cae8e810640"
    
    try:
        response = requests.get(graph_url)
        response.raise_for_status()
        
        # Send the avatar image to the user with a caption
        caption = f"<b>Avatar cho Facebook ID hoặc link</b>: <code>{facebook_id}</code>"
        bot.send_photo(message.chat.id, response.url, caption=caption, parse_mode='html')
        
        # Xóa tin nhắn chờ sau khi hoàn thành
        bot.delete_message(message.chat.id, waiting_message.message_id)
    
    except requests.RequestException as e:
        bot.edit_message_text(f'Có lỗi xảy ra khi truy cập Facebook: {e}', message.chat.id, waiting_message.message_id)
    except Exception as e:
        bot.edit_message_text(f'Có lỗi xảy ra: {e}', message.chat.id, waiting_message.message_id)


def check_car_info(bsx):
    url = f'https://vietcheckcar.com/api/api.php?api_key=sfund&bsx={bsx}&bypass_cache=0&loaixe=1&vip=0'
    response = requests.get(url)
    return response.json()

@bot.message_handler(commands=['vi_pham'])
def handle_check(message):
    try:
        # Lấy biển số từ tin nhắn
        bsx = message.text.split()[1]
        # Gọi API và lấy kết quả
        car_info = check_car_info(bsx)

        # Kiểm tra nếu có vi phạm
        if car_info.get('totalViolations', 0) > 0:
            # Lấy thông tin vi phạm đầu tiên
            violation = car_info['violations'][0]

            # Trích xuất thông tin từ JSON
            bien_so = violation.get('bien_kiem_sat', 'N/A')
            trang_thai = violation.get('trang_thai', 'N/A')
            mau_bien = violation.get('mau_bien', 'N/A')
            loai_phuong_tien = violation.get('loai_phuong_tien', 'N/A')
            thoi_gian_vi_pham = violation.get('thoi_gian_vi_pham', 'N/A')
            dia_diem_vi_pham = violation.get('dia_diem_vi_pham', 'N/A')
            hanh_vi_vi_pham = violation.get('hanh_vi_vi_pham', 'N/A')
            don_vi_phat_hien_vi_pham = violation.get('don_vi_phat_hien_vi_pham', 'N/A')
            noi_giai_quyet_vu_viec = violation.get('noi_giai_quyet_vu_viec', 'N/A').replace('\\n', '\n')  # Xử lý \n trong JSON
            so_dien_thoai = violation.get('so_dien_thoai', 'N/A')
            muc_phat = violation.get('muc_phat', 'N/A')

            # Định dạng tin nhắn
            message_text = f'''
<blockquote expandable>┏━━━━━━━━━━━━━━━━━━━━━━━━┓
━━━━━━━━━𝙏𝙝𝙤̂𝙣𝙜 𝙩𝙞𝙣 𝙫𝙞 𝙥𝙝𝙖̣𝙢━━━━━━━━
┗━━━━━━━━━━━━━━━━━━━━━━━━┛
» Biển số: {bien_so}

» Trạng thái: {trang_thai}

» Màu biển: {mau_bien}

» Loại phương tiện: {loai_phuong_tien}

» Thời gian vi phạm: {thoi_gian_vi_pham}

» Địa điểm vi phạm: {dia_diem_vi_pham}

» Hành vi vi phạm: {hanh_vi_vi_pham}

» Đơn vị phát hiện vi phạm: {don_vi_phat_hien_vi_pham}

» Nơi giải quyết vụ việc: {noi_giai_quyet_vu_viec}</blockquote>'''

            # Gửi tin nhắn với thông tin
            bot.send_message(message.chat.id, {message_text}, parse_mode="HTML")

        else:
            bot.send_message(message.chat.id, f"<blockquote>Biển số xe {bsx} không có lỗi vi phạm.</blockquote>", parse_mode="HTML")

    except IndexError:
        bot.send_message(message.chat.id, "Vui lòng nhập biển số xe. Ví dụ: /bsx 24A14307")
    except Exception as e:
        bot.send_message(message.chat.id, f"Lỗi: {str(e)}")


@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    # Lấy nội dung văn bản sau lệnh /voice
    text = message.text[len('/voice '):].strip()

    # Nếu không có văn bản, trả lời hướng dẫn sử dụng
    if not text:
        bot.reply_to(message, "🤖 Tqhuy-BOT\nUsage: /voice <Text>")
        return

    # Tạo tệp tạm thời để lưu file .mp3 với tên "elven"
    temp_file_path = tempfile.mktemp(suffix='elven.mp3')

    try:
        # Chuyển văn bản thành giọng nói bằng gTTS
        tts = gTTS(text, lang='vi')
        tts.save(temp_file_path)

        # Mở và gửi file âm thanh .mp3 với tên "elven"
        with open(temp_file_path, 'rb') as audio_file:
            bot.send_voice(chat_id=message.chat.id, voice=audio_file)

    except Exception as e:
        bot.reply_to(message, "🤖 Tqhuy-BOT\nError Bot")
    
    finally:
        # Xóa tệp âm thanh tạm thời sau khi gửi
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@bot.message_handler(commands=['qr'])
def generate_qr(message):
    # Tách từ khóa nhập vào lệnh
    input_text = message.text.split(maxsplit=1)
    
    if len(input_text) > 1:
        input_text = input_text[1]  # Lấy phần từ khóa sau /qr
        # Tạo QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(input_text)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        bio = BytesIO()
        bio.name = 'qr.png'
        img.save(bio, 'PNG')
        bio.seek(0)

        # Gửi ảnh QR tới người dùng
        bot.send_photo(message.chat.id, photo=bio, caption=f"<blockquote>QR của chữ: {input_text}</blockquote>",parse_mode="HTML")
    else:
        bot.reply_to(message, "🤖 Tqhuy-BOT\n🤖 Usage: /qr <Chữ Cần Tạo QR>")


# Sử lí GetKey
from datetime import datetime

def TimeStamp():
    now = datetime.now().date()  # Đúng cách lấy ngày hiện tại
    return now

def get_time_vietnam():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def init_db():
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            key TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

init_db()


# Thiết lập cơ sở dữ liệu
def setup_database():
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            key TEXT,
            has_used_key INTEGER DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

setup_database()


print("truongdeptraivcll đã  đang hoạt động")
@bot.message_handler(commands=['ngl'])
def send_ngl_message(message):
    try:
        args = message.text.split(' ', 3)
        if len(args) < 4:
            bot.reply_to(message, "⚠️ Vui lòng cung cấp username, message, và amount. Sử dụng: /ngl {username} {message} {amount}")
            return

        # Extract parameters from the message
        username = args[1]
        message_text = args[2]
        amount = args[3]

        # Call the API with provided parameters
        response = send_api_request(username, message_text, amount)
        
        if response.status_code == 200:
            bot.reply_to(message, f"✅ Thông điệp đã được gửi thành công đến `{username}`.")
        else:
            bot.reply_to(message, f"❌ Có lỗi xảy ra khi gửi tin nhắn: {response.text}")

    except Exception as e:
        bot.reply_to(message, f"❌ Có lỗi xảy ra: {e}")

def send_api_request(username, message_text, amount):
    # Format the URL with parameters
    url = API_URL.format(username=username, message=message_text, amount=amount)
    response = requests.get(url)
    return response


@bot.message_handler(commands=['getkey'])
def startkey(message):
    bot.reply_to(message, text='Chờ đi địt mẹ mày!')
    today = datetime.now().date()  # Lấy ngày hôm nay
    key = "truong" + str(int(message.from_user.id) * int(today.day) - 12666)
    key = "https://xuantruong.x10.mx/key.html?key=" + key
    api_token = '57c63df502654edce2a31052a45d72fa29e49cc17bd6db0ec88ded91dff0cb00'
    
    try:
        response = requests.get(f'https://yeumoney.com/QL_api.php?token={api_token}&format=json&url={key}')
        url = response.json()

        # Check if the 'shortenedUrl' key exists in the response JSON
        if 'shortenedUrl' in url:
            url_key = url['shortenedUrl']
        else:
            bot.reply_to(message, 'Không tìm thấy shortenedUrl trong phản hồi.')
            return

    except requests.RequestException as e:
        bot.reply_to(message, 'Đã xảy ra lỗi khi kết nối đến API.')
        print(f"Request error: {e}")
        return

    text = f'''
- LINK LẤY KEY CỦA @{message.from_user.username} NGÀY {today} LÀ: {url_key} 
- KHI LẤY KEY XONG, DÙNG LỆNH /key <key> ĐỂ TIẾP TỤC -
    '''
    bot.reply_to(message, text)
@bot.message_handler(commands=['plan'])
def check_plan(message):
    user_id = message.from_user.id

    # Kiểm tra trạng thái "đã get"
    if user_id in used_getkey_users:
        key_status = " Đã /getkey "
    else:
        key_status = " Chưa /getkey "

    # Kiểm tra VIP qua thư mục
    vip_file_path = os.path.join(vip_folder_path, f"{user_id}.txt")
    if os.path.exists(vip_file_path):
        vip_status = " Đã Mua Vip "
    else:
        vip_status = " Chưa Mua Vip "

    # Trả về kết quả
    plan_message = f"""<blockquote> Name Bot : [ @ddoslo_bot ]
    thằng óc l tên @{message.from_user.username}
    _______________________________________________________
    Trạng thái Free : /spam  của bạn : [ {key_status} ] 
    _______________________________________________________
    Trạng thái VIP  : /smsvip /spamvip [ {vip_status} ] </blockquote>"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
      types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),
        
    )

    video_url = "https://files.catbox.moe/xbgx14.mp4"
    bot.send_video(message.chat.id, video_url, caption=plan_message, parse_mode='HTML', reply_markup=keyboard)
    

# Tạo thư mục VIP nếu chưa tồn tại
if not os.path.exists(vip_folder_path):
    os.makedirs(vip_folder_path)


import string

# Đảm bảo thư mục ./user tồn tại
if not os.path.exists('./user'):
    os.makedirs('./user')

# Tạo một key ngẫu nhiên
def generate_key():
    """Tạo một key ngẫu nhiên gồm 16 ký tự (chữ và số)."""
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return key

# Lưu key và thời gian hết hạn vào tệp tin của người dùng
def save_key_for_user(user_id, key, expiry):
    """Lưu key và thời gian hết hạn vào tệp của người dùng."""
    user_file = f'./user/{user_id}_key.txt'
    
    # Lưu thông tin key và hạn sử dụng vào tệp
    with open(user_file, 'w', encoding='utf-8') as file:
        file.write(f'Key: {key}\nExpiry: {expiry.strftime("%H:%M %d-%m-%Y")}\n')
    
    return user_file  # Trả về đường dẫn tệp vừa lưu


@bot.message_handler(commands=['taokey'])
def create_key(message):
    if str(message.from_user.id) == ADMIN_ID:
        try:
            command_parts = message.text.split(' ', 2)  # Tách thành ba phần: lệnh, mã thẻ, thời gian
            if len(command_parts) < 3:
                bot.reply_to(message, "Vui lòng nhập mã thẻ và thời gian hết hạn. Ví dụ: /taokey 123123 23:00 2-2-2024")
                return

            # Lấy mã thẻ và thời gian
            card_serial = command_parts[1]
            expiry_time_str = command_parts[2]
            
            # Chuyển đổi thời gian từ chuỗi thành đối tượng datetime
            expiry = datetime.strptime(expiry_time_str, '%H:%M %d-%m-%Y')

            # Tạo key ngẫu nhiên
            new_key = generate_key()

            # Lưu key vào tệp cho người dùng (admin có thể lưu key cho người khác nếu cần)
            save_key_for_user(message.from_user.id, new_key, expiry)

            # Gửi thông báo cho admin về key mới
            bot.send_message(ADMIN_ID, f"Admin {message.from_user.username} đã tạo key:\n"
                                       f"Key: {new_key}\n"
                                       f"Serial: {card_serial}\n"
                                       f"Hạn sử dụng: {expiry.strftime('%H:%M %d-%m-%Y')}\n")

            # Phản hồi cho admin
            bot.reply_to(message, f"Key đã được tạo: {new_key}\nSerial: {card_serial}\nHạn sử dụng: {expiry.strftime('%H:%M %d-%m-%Y')}")
            
        except Exception as e:
            bot.reply_to(message, f"Đã xảy ra lỗi khi tạo key: {e}")
    else:
        bot.reply_to(message, "Bạn không có quyền sử dụng lệnh này.")

@bot.message_handler(commands=['key'])
def key(message):
    # Split the message and check if the key argument is provided
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'VUI LÒNG NHẬP KEY ĐÚNG ĐỊNH DẠNG: /key <key>')
        return

    user_id = message.from_user.id
    key = message.text.split()[1]
    today = datetime.now().date()  # Lấy ngày hôm nay
    expected_key = "truong" + str(int(user_id) * int(today.day) - 12666)

    # Log the expected and user-entered keys for debugging
    print(f"Expected key: {expected_key}")
    print(f"User-entered key: {key}")
    
    # Compare the key entered by the user with the expected key
    if key == expected_key:
        bot.reply_to(message, 'KEY HỢP LỆ. BẠN ĐÃ ĐƯỢC PHÉP SỬ DỤNG LỆNH /spam.')
        
        # Ensure the directory exists before writing to the file
        file_path = f'./user/{today.day}/{user_id}.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write an empty file to indicate that the key is valid
        with open(file_path, "w") as fi:
            fi.write("")  # Can add more data to the file if needed
    else:
        bot.reply_to(message, 'KEY KHÔNG HỢP LỆ.')


@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    today = date.today()
    
    user_directory = f"./user/{today.day}/"
    user_file_path = os.path.join(user_directory, f"{user_id}.txt")

    # Check if the directory exists, create if not
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    if not os.path.exists(user_file_path):
        bot.reply_to(message, '*Vui lòng GET KEY của ngày hôm nay* -Dùng /getkey để lấy key và dùng /key để nhập key hôm nay.')
        return

    # Check for phone number and spam count
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI')
        return

    phone_number = message.text.split()[1]
    
    # Validate phone number format
    if not re.search(r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return

    # Block specific phone numbers (e.g., admin's number)
    if phone_number in ["0377323188"]:
        bot.reply_to(message, "Spam số admin à tao ban mày giờ 😾")
        return

    # Paths to external scripts
    script_files = ["text1.py", "text2.py", "text3.py", "text4.py"]

    # Cooldown mechanism (120 seconds per user)
    username = message.from_user.username
    current_time = time.time()

    # Check if user is within cooldown period
    if username in cooldown_dict and current_time - cooldown_dict[username].get('free', 0) < 220:
        remaining_time = int(220 - (current_time - cooldown_dict[username].get('free', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /spam.")
        return
    
    # Update cooldown dictionary
    cooldown_dict[username] = {'free': current_time}

    # Execute external scripts concurrently
    for script_file in script_files:
        script_path = os.path.join(os.getcwd(), script_file)
        process = subprocess.Popen(["python", script_path, phone_number, "2"])
        processes.append(process)

    # Timestamp for the message
    thoigian = dt.now().strftime('%d-%m-%Y %H:%M:%S')
    
    # Video URL and message text
    
    xinchao = f"""<blockquote>
╭────────────────────⪢۰۪۪۫۫●۪۫۰
├⪢🪪| Yêu Cầu Bởi: @{username}
├⪢🚀| Trạng Thái: Thành Công
├⪢⏱| |THỜI GIAN: concac
├⪢🪧 | GÓI: MIỄN PHÍ
├⪢👮‍♂️| Owner: @ngotk999
╰────────────────────⪢۰۪۪۫۫●۪۫۰ 
</blockquote>
     """
    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
      types.InlineKeyboardButton("👤 Admin", url="https://t.me/ngotk999"),        
    )

    video_url = "https://files.catbox.moe/xbgx14.mp4"
    bot.send_video(message.chat.id, video_url, caption=xinchao, parse_mode='HTML', reply_markup=keyboard)

    # Gửi tin nhắn "loading"
    sent_message = bot.reply_to(message, "Đang xử lý...")

    # Chuỗi hiệu ứng "Loading"
    
    loading_frames = [
        "Buy GÌ Cứ Ib @ngotk999 dcu ",
        "cái địt mẹ mày  ...",        
    ]
    

    # Hiệu ứng "Loading"
    for _ in range(1):  # Lặp 3 lần hiệu ứng
        for frame in loading_frames:
            bot.edit_message_text(frame, chat_id=message.chat.id, message_id=sent_message.message_id)
            time.sleep(0.2)

    # Cập nhật trạng thái spam
    bot.edit_message_text(f"\n\n[ {filename} ] Bắt Đầu Spam  {phone_number}  ", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(1)  # Chờ trước khi xóa

    # Xóa tin nhắn cũ
    bot.delete_message(message.chat.id, message.message_id)  # Xóa tin nhắn lệnh gốc
    bot.delete_message(message.chat.id, sent_message.message_id)  # Xóa tin nhắn "loading"




def generate_key():
    return str(dt.now().strftime('%Y%m%d%H%M%S'))

# Lưu key cho người dùng vào file
def save_key_for_user(user_id, key, expiry_time):
    user_directory = f"./user/keys/"
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    with open(f"{user_directory}napthe.txt", "a") as f:
        f.write(f"{user_id} {key} {expiry_time}\n")

# Tải key của người dùng
def load_key_for_user(user_id):
    try:
        with open("./user/keys/napthe.txt", "r") as f:
            for line in f.readlines():
                parts = line.split(" ")
                stored_user_id, key, expiry_time = parts[0], parts[1], parts[2]
                if stored_user_id == str(user_id):
                    return key, expiry_time
    except FileNotFoundError:
        return None, None
    return None, None

@bot.message_handler(commands=['taokey'])
def create_key(message):
    if str(message.from_user.id) == ADMIN_ID:
        try:
            command_parts = message.text.split(' ', 1)
            if len(command_parts) < 2:
                bot.reply_to(message, "Vui lòng nhập thời gian hết hạn.")
                return

            expiry_time_str = command_parts[1]
            expiry = dt.strptime(expiry_time_str, '%H:%M %d-%m-%Y')

            new_key = generate_key()
            save_key_for_user(message.from_user.id, new_key, expiry)

            # Gửi thông báo cho admin về key mới
            bot.send_message(ADMIN_ID, f"Admin {message.from_user.username} đã tạo key:\nKey: {new_key}\nHạn sử dụng: {expiry.strftime('%H:%M %d-%m-%Y')}")
            
            bot.reply_to(message, f"Key đã được tạo: {new_key}, Hạn sử dụng: {expiry.strftime('%H:%M %d-%m-%Y')}")
        except Exception as e:
            bot.reply_to(message, f"Đã xảy ra lỗi khi tạo key: {e}")
    else:
        bot.reply_to(message, "Bạn không có quyền sử dụng lệnh này.")

@bot.message_handler(commands=['enkey'])
def set_key(message):
    user_id = message.from_user.id
    input_key = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not input_key:
        bot.reply_to(message, 'Vui lòng nhập key.')
        return

    # Kiểm tra key hợp lệ
    key, _ = load_key_for_user(user_id)
    if key is None:
        bot.reply_to(message, "Bạn chưa có key hợp lệ. Vui lòng dùng /taokey để lấy key.")
        return

    if input_key != key:
        bot.reply_to(message, "Key bạn nhập không hợp lệ.")
        return

    expiry_time = dt.strptime(_, '%H:%M %d-%m-%Y')
    current_time = dt.now()

    if current_time > expiry_time:
        bot.reply_to(message, "Key của bạn đã hết hạn. Vui lòng nhập lại key mới.")
        return

    bot.reply_to(message, "Key hợp lệ. Bạn có thể sử dụng lệnh /spam.")

@bot.message_handler(commands=['spams'])
def spam(message):
    user_id = message.from_user.id
    today = date.today()

    user_directory = f"./user/{today.day}/"
    user_file_path = os.path.join(user_directory, f"{user_id}.txt")

    # Kiểm tra xem người dùng có key hợp lệ chưa
    key, _ = load_key_for_user(user_id)
    if key is None:
        bot.reply_to(message, '*Vui lòng GET KEY của ngày hôm nay* -Dùng /taokey để lấy key và dùng /key để nhập key hôm nay.')
        return

    # Kiểm tra xem người dùng đã nhập số điện thoại chưa
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI')
        return

    phone_number = message.text.split()[1]

    # Kiểm tra định dạng số điện thoại
    if not re.search(r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return

    # Kiểm tra thời gian hết hạn của key
    expiry_time_str = _  # Giả sử chúng ta lấy thời gian hết hạn từ key đã lưu
    expiry_time = dt.strptime(expiry_time_str, '%H:%M %d-%m-%Y')
    current_time = dt.now()

    if current_time > expiry_time:
        bot.reply_to(message, "Key của bạn đã hết hạn. Vui lòng nhập lại key mới.")
        return

    # Block specific phone numbers (e.g., admin's number)
    if phone_number in ["0377323188"]:
        bot.reply_to(message, "Spam số admin à tao ban mày giờ 😾")
        return

    # Tiến hành spam
    bot.reply_to(message, f"Đang tiến hành spam số {phone_number}...")

    # Tạo tin nhắn thông báo đã spam
    bot.send_message(message.chat.id, f"Đã spam số {phone_number} thành công!")



    #free spam tạo key


@bot.message_handler(commands=['stop_spam'])
def stop_spam(message):
    user_id = message.from_user.id
    username = message.from_user.username
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Vui Lòng Nhập Số Điện Thoại Để Dừng Spam.')
        return
    phone_number = message.text.split()[1]
    stop_spam_for_phone(phone_number)
    video_url = "liemspam.000webhostapp.com/lon.mp4"
    bot.reply_to(message, f"""
┌──────⭓ {name_bot} ⭓──────
│» User: @{username}                      
│» Stop: Success [✓]
│» Attacking: {phone_number}
└────────────[✓]─────────
    """)
    
def stop_spam_for_phone(phone_number):
    for process in processes:
        if phone_number in process.args:
            process.terminate()
            processes.remove(process)
import os

@bot.message_handler(commands=['addbasic'])
def addbasic(message):
    # Ensure admin access
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Bạn không có quyền sử dụng lệnh này.")
        return

    # Check if a user ID or username is provided
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Vui lòng nhập ID người dùng hoặc tên đăng nhập để thêm.')
        return

    user_identifier = message.text.split()[1]

    # Ensure 'basic' folder exists
    basic_folder_path = "./basic"
    if not os.path.exists(basic_folder_path):
        os.makedirs(basic_folder_path)

    # Create a basic user file for the user
    basic_file_path = f"{basic_folder_path}/{user_identifier}.txt"
    if not os.path.exists(basic_file_path):  # Avoid overwriting existing user
        with open(basic_file_path, 'w') as file:
            file.write("basic_user")
        bot.reply_to(message, f"Người dùng {user_identifier} đã được thêm vào danh sách Basic.")
        print(f"Added user {user_identifier} to basic folder.")
    else:
        bot.reply_to(message, f"Người dùng {user_identifier} đã có trong danh sách Basic rồi.")
        print(f"User {user_identifier} already exists in basic folder.")


@bot.message_handler(commands=['spambasic'])
def spambasic(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    user_id = message.from_user.id
    basic_file_path = f"./basic/{user_id}.txt"

    # Check if user has access to use /spambasic
    if not os.path.exists(basic_file_path):
        bot.reply_to(message, "Bạn chưa có quyền sử dụng lệnh này. Vui lòng liên hệ admin.")
        return

    # Ensure phone number argument is provided
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Vui lòng nhập số điện thoại.')
        return

    phone_number = message.text.split()[1]

    # Validate phone number format
    if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'Số điện thoại không hợp lệ!')
        return


    # Paths to external scripts
    script_files = ["text1.py", "text2.py", "text3.py", "text4.py", "text5.py", "text6.py", "text7.py", "text8.py", "text9.py", "text10.py"]
    
    # Execute external scripts without cooldown
    for script_file in script_files:
        script_path = os.path.join(os.getcwd(), script_file)
        subprocess.Popen(["python", script_path, phone_number, "50"])

    print(f"user vip User ID: {user_id}, Name: {full_name}, Phone: {phone_number}, Count: 100 ")
    # Send confirmation to user
    response = (
        f"Attack initiated 🚀\n"
        f"+ Target number 📱: [{phone_number}]\n"
        f"+ Number of attacks 📱: [ 999 ]"
    )
    sent_message = bot.reply_to(message, response)
    bot.reply_to(message,response)
    # Short delay to ensure the bot has sent the reply
    # Wait for a moment before the next part of the "shattering" effect
    
    bot.edit_message_text(f"\n\n ! ", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    # Another effect stage (disintegration)
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading .", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(1)
    
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading .", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading .", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ..", chat_id=message.chat.id, message_id=sent_message.message_id)
    
    time.sleep(0.2)
    bot.edit_message_text(f"\n\n Loading ...", chat_id=message.chat.id, message_id=sent_message.message_id)
    time.sleep(0.2)

    bot.edit_message_text(f"\n\n[ {full_name} ] Bắt Đầu Spam  {phone_number}  ", chat_id=message.chat.id, message_id=sent_message.message_id)
    # Another effect stage (disintegration)
    time.sleep(1)
    bot.delete_message(message.chat.id, message.message_id)  # Delete the original message
    bot.delete_message(sent_message.chat.id, sent_message.message_id)



@bot.message_handler(commands=['info'])
def handle_check(message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    
    # Hiển thị biểu tượng đợi
    waiting = bot.reply_to(message, "🔎")
    
    # Lấy thông tin người dùng
    user_photos = bot.get_user_profile_photos(user.id)
    chat_info = bot.get_chat(user.id)
    chat_member_status = bot.get_chat_member(message.chat.id, user.id).status
    
    bio = chat_info.bio or "Không có bio"
    user_first_name = user.first_name
    user_last_name = user.last_name or ""
    user_username = f"@{user.username}" if user.username else "Không có username"
    user_language = user.language_code or 'Không xác định'
    
    # Định nghĩa trạng thái người dùng
    status_dict = {
        "creator": "Admin chính",
        "administrator": "Admin",
        "member": "Thành viên",
        "restricted": "Bị hạn chế",
        "left": "Rời nhóm",
        "kicked": "Bị đuổi khỏi nhóm"
    }
    status = status_dict.get(chat_member_status, "Không xác định")
    
    # Soạn tin nhắn gửi đi
    caption = (
        "<pre>     🚀 THÔNG TIN 🚀\n"
        "┌──────────⭓INFO⭓─────────\n"
        f"│» 🆔: {user.id}\n"
        f"│» 👤Tên: {user_first_name} {user_last_name}\n"
        f"│» 👉Username: {user_username}\n"
        f"│» 🔰Ngôn ngữ: {user_language}\n"
        f"│» 🏴Trạng thái: {status}\n"
        f"│» ✍️Bio: {bio}\n"
        f"│» 🤳Avatar: {'Đã có avatar' if user_photos.total_count > 0 else 'Không có avatar'}\n"
        "└───────────────[✓]─────────────</pre>"
    )
    
    # Gửi ảnh hoặc tin nhắn văn bản
    if user_photos.total_count > 0:
        bot.send_photo(message.chat.id, user_photos.photos[0][-1].file_id, caption=caption, parse_mode='HTML', reply_to_message_id=message.message_id)
    else:
        bot.reply_to(message, caption, parse_mode='HTML')
    
    # Xóa tin nhắn chờ sau khi hoàn tất
    def xoatn(message, delay):
        try:
            bot.delete_message(message.chat.id, waiting.message_id)
        except Exception as e:
            print(f"Lỗi khi xóa tin nhắn: {e}")
    
    threading.Thread(target=xoatn, args=(message, 0)).start()

@bot.message_handler(commands=['check'])
def check_hot_web(message):
    # Kiểm tra xem lệnh có đủ tham số không (URL của trang web cần kiểm tra)
    if len(message.text.split()) < 2:
        bot.reply_to(message, '<blockquote>Vui lòng cung cấp URL của trang web cần kiểm tra (VD: /check https://example.com).</blockquote>',parse_mode='HTML')
        return
    
    # Lấy URL từ lệnh
    url = message.text.split()[1]

    try:
        # Gửi yêu cầu HTTP GET đến URL
        response = requests.get(url, timeout=10)
        
        # Kiểm tra trạng thái của trang web
        if response.status_code == 200:
            bot.reply_to(message, f"<blockquote>🔗 Trang web {url} đang hoạt động bình thường (Status: 200 OK).</blockquote>", parse_mode='HTML')
        else:
            bot.reply_to(message, f"<blockquote>⚠️ Trang web {url} có vấn đề (Status: {response.status_code}).</blockquote>", parse_mode='HTML')
    except requests.exceptions.RequestException as e:
        # Xử lý lỗi nếu không thể kết nối tới trang web
        bot.reply_to(message, f"<blockquote>❌ Không thể kết nối tới trang web {url}. Lỗi: {e}</blockquote>", parse_mode='HTML')

@bot.message_handler(commands=['checkip'])
def check_ip(message):
    # Lấy các tham số từ lệnh
    params = message.text.split()
    
    if len(params) < 2:
        bot.reply_to(message, 'Vui lòng cung cấp địa chỉ IP cần kiểm tra (VD: /checkip 8.8.8.8).')
        return
    
    ip_address = params[1]

    try:
        # Gửi yêu cầu tới dịch vụ API để lấy thông tin chi tiết về địa chỉ IP
        response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=10)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        # Lấy dữ liệu từ phản hồi
        ip_data = response.json()

        # Trích xuất thông tin chi tiết
        city = ip_data.get('city', 'Không xác định')
        region = ip_data.get('region', 'Không xác định')
        country = ip_data.get('country', 'Không xác định')
        org = ip_data.get('org', 'Không xác định')
        loc = ip_data.get('loc', 'Không xác định')
        
        # Tạo thông tin để gửi cho người dùng
        ip_info = (f"<blockquote>🌐 Địa chỉ IP: {ip_address}\n"
                   f"📍 Thành phố: {city}\n"
                   f"🏛 Khu vực: {region}\n"
                   f"🌎 Quốc gia: {country}\n"
                   f"🏢 Tổ chức: {org}\n"
                   f"📍 Vị trí (Lat, Lng): {loc}</blockquote>")
        
        # Gửi thông tin địa chỉ IP tới người dùng
        bot.reply_to(message, ip_info, parse_mode='HTML')
    except requests.exceptions.RequestException as e:
        # Xử lý lỗi nếu không thể kết nối đến dịch vụ API
        bot.reply_to(message, f"<blockquote>❌ Không thể kết nối tới dịch vụ kiểm tra IP. Lỗi: {e}</pre>", parse_mode='blockquote')
    except Exception as e:
        # Xử lý các lỗi khác
        bot.reply_to(message, f"<blockquote>❌ Đã xảy ra lỗi khi kiểm tra IP. Lỗi: {e}</pre>", parse_mode='blockquote')

@bot.message_handler(commands=['html'])
def handle_code_command(message):
    # Tách lệnh và URL từ tin nhắn
    command_args = message.text.split(maxsplit=1)

    # Kiểm tra xem URL có được cung cấp không
    if len(command_args) < 2:
        bot.reply_to(message, "Vui lòng cung cấp url sau lệnh /html. Ví dụ: /html https://example.com")
        return

    url = command_args[1]
    
    # Kiểm tra xem URL có hợp lệ không
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        bot.reply_to(message, "Vui lòng cung cấp một URL hợp lệ.")
        return

    domain = parsed_url.netloc
    file_name = f"tqhuygethtml.txt"
    
    try:
        # Lấy nội dung HTML từ URL
        response = requests.get(url)
        response.raise_for_status()  # Xảy ra lỗi nếu có lỗi HTTP

        # Lưu nội dung HTML vào file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # Định dạng HTML và gửi file về người dùng
        with open(file_name, 'rb') as file:
            caption = f"<blockquote>HTML của trang web:\n{url}</blockquote>"
            bot.send_document(message.chat.id, file, caption=caption, parse_mode='HTML')

    except requests.RequestException as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi tải trang web: {e}")

    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi xử lý file: {e}")

    finally:
        # Đảm bảo xóa file sau khi gửi
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                bot.reply_to(message, f"Đã xảy ra lỗi khi xóa file: {e}")


#sử lí lệnh mở mõm và khóa mõ
@bot.message_handler(commands=['im'])
def warn_user(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    
    # Kiểm tra xem tin nhắn có chứa thông tin cần thiết không
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>Ơ !!!</blockquote>', parse_mode='HTML')
        return

    user_id = message.reply_to_message.from_user.id
    
    try:
        # Cấm chat người dùng trong 15 phút
        until_date = int(time.time()) + 15 * 60
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            until_date=until_date
        )
        
        # Gửi tin nhắn thông báo người dùng đã bị cấm chat trong 15 phút
        bot.send_message(
            message.chat.id, 
            f"<blockquote>⚠️ Người dùng với ID {user_id} đã bị cảnh báo và cấm chat trong 15 phút.</blockquote>",
            parse_mode='HTML'
        )
    except Exception as e:
        # Nếu có lỗi xảy ra
        bot.reply_to(message, "<blockquote>Không thể cảnh báo người dùng. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>", parse_mode='HTML')
        print(f"Error warning user: {e}")

@bot.message_handler(commands=['unim'])
def unrestrict_user(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    
    # Kiểm tra xem tin nhắn có chứa thông tin cần thiết không
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>Vui lòng trả lời tin nhắn của người dùng cần hủy cấm chat.</blockquote>', parse_mode='HTML')
        return

    user_id = message.reply_to_message.from_user.id
    
    try:
        # Gỡ bỏ hạn chế chat cho người dùng
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            until_date=0  # Không cấm chat nữa
        )
        
        # Gửi tin nhắn thông báo người dùng đã được phép chat trở lại
        bot.send_message(
            message.chat.id, 
            f"<blockquote>✅ Người dùng với ID {user_id} đã được phép chat trở lại.</blockquote>", 
            parse_mode='HTML'
        )
    except Exception as e:
        # Nếu có lỗi xảy ra
        bot.reply_to(message, '<blockquote>Không thể gỡ cấm chat cho người dùng. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>', parse_mode='HTML')
        print(f"Error unrestricted user: {e}")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    
    # Kiểm tra xem tin nhắn có chứa thông tin cần thiết không
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>........</blockquote>', parse_mode='HTML')
        return

    user_id = message.reply_to_message.from_user.id
    
    try:
        # Bot thực hiện lệnh ban người dùng
        bot.kick_chat_member(message.chat.id, user_id)
        
        # Gửi tin nhắn thông báo người dùng đã bị ban
        bot.send_message(
            message.chat.id, 
            f"<blockquote>🔨 Người dùng với ID {user_id} đã bị ban khỏi nhóm.</blockquote>",
            parse_mode='HTML'
        )
    except Exception as e:
        # Nếu có lỗi xảy ra
     bot.reply_to(message, '<blockquote>Không thể ban người dùng. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>', parse_mode='HTML')

bot_active = True

from datetime import datetime
from io import BytesIO

@bot.message_handler(commands=['tiktok'])
def tiktok_download(message):
    try:
        waiting_message = bot.reply_to(message, '⌨️ Đang tải video...')

        url = message.text.split(' ')[1]
        api_url = f"https://subhatde.id.vn/tiktok/downloadvideo?url={url}"
        
        response = requests.get(api_url)
        data = response.json()
        
        if data['code'] == 0:
            video_data = data['data']
            author = video_data.get('author', {})

            title = video_data.get('title', 'Không có tiêu đề')
            region = video_data.get('region', 'Không rõ khu vực')
            play_url = video_data.get('play', 'Không có URL phát video')
            music_url = video_data.get('music', 'Không có URL nhạc')
            create_time = video_data.get('create_time', 0)
            nickname = author.get('nickname', 'Không có tên tác giả')

            create_time_formatted = datetime.utcfromtimestamp(create_time).strftime('%H:%M:%S | %d/%m/%Y')

            haha = (
                f"<b>🎥 {title}</b>\n\n"
                f"<blockquote>\n"
                f"📅 Ngày Đăng: {create_time_formatted}\n\n"
                f"👤 <b>Tác giả:</b> {nickname}\n"
                f"🌍 <b>Khu Vực:</b> {region}\n"
                f"⏱️ <b>Độ Dài Video:</b> {video_data.get('duration', 'Không rõ')} Giây\n\n"
                f"👁 <b>Views:</b> {video_data.get('play_count', 0):,}\n"
                f"❤️ <b>Likes:</b> {video_data.get('digg_count', 0):,}\n"
                f"💬 <b>Comments:</b> {video_data.get('comment_count', 0):,}\n"
                f"🔗 <b>Shares:</b> {video_data.get('share_count', 0):,}\n"
                f"📥 <b>Downloads:</b> {video_data.get('download_count', 0):,}\n"
                f"📑 <b>Lưu vào bộ sưu tập:</b> {video_data.get('collect_count', 0):,}\n"
                f"</blockquote>"
                f"🎵 <a href='{music_url}'>Nhạc By Video</a>"
            )

            # Send video
            bot.send_video(chat_id=message.chat.id, video=play_url, caption=haha, parse_mode='HTML')

            # Send audio
            music_response = requests.get(music_url)
            audio_data = BytesIO(music_response.content)
            audio_data.seek(0)
            bot.send_audio(message.chat.id, audio_data, title="Nhạc nền từ video", performer=nickname)

        else:
            bot.send_message(message.chat.id, "Không thể lấy thông tin video từ TikTok.")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra: {str(e)}")
    finally:
        # Ensure the waiting message is deleted whether there's an error or not
        try:
            bot.delete_message(message.chat.id, waiting_message.message_id)
        except Exception:
            pass


AVATAR_NAMES = {
    102000012: "Chiến binh huyền thoại",
    102000013: "Anh hùng ánh sáng",
}

CLOTHES_NAMES = {
    "211000000": "Áo giáp sắt",
    "205000646": "Quần chiến binh",
    "211000168": "Mũ quyền năng",
    "204000523": "Giày thần tốc",
}

# Xử lý lệnh /ff
@bot.message_handler(commands=['ff'])
def send_gai_image(message):
    chat_id = message.chat.id

    # Lấy tham số ID từ tin nhắn
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, "Vui lòng cung cấp ID! Cú pháp: /ff <id>")
        return

    input_id = command_parts[1]  # Lấy ID từ tham số
    api_url = f"https://elevenbotbythaihoc.us.kg/api/apiff.php/?id={input_id}&key=freeth"

    try:
        # Gửi yêu cầu API
        response = requests.get(api_url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Giả sử API trả về JSON

        if not data.get("error"):
            basic_info = data.get("data", {}).get("basicInfo", {})
            profile_info = data.get("data", {}).get("profileInfo", {})
            pet_info = data.get("data", {}).get("petInfo", {})
            social_info = data.get("data", {}).get("socialInfo", {})

            # Định dạng thông tin
            result = (
                f"*Kết quả từ API:*\n\n"
                f"📄 *Thông tin cơ bản:*\n"
                f"- Account ID: `{basic_info.get('accountId', 'N/A')}`\n"
                f"- Tên nhân vật: `{basic_info.get('nickname', 'N/A')}`\n"
                f"- Khu vực: `{basic_info.get('region', 'N/A')}`\n"
                f"- Cấp độ: `{basic_info.get('level', 'N/A')}`\n"
                f"- Rank hiện tại: `{basic_info.get('rank', 'N/A')}`\n"
                f"- Điểm xếp hạng: `{basic_info.get('rankingPoints', 'N/A')}`\n\n"

                f"👕 *Hồ sơ:*\n"
                f"- Avatar ID: `{profile_info.get('avatarId', 'N/A')}`\n"
                f"- Trang phục: {', '.join(profile_info.get('clothes', []))}\n"
                f"- Kỹ năng được trang bị: "
                f"{', '.join(str(skill.get('skillId', 'N/A')) for skill in profile_info.get('equippedSkills', []))}\n\n"

                f"🐾 *Thông tin thú cưng:*\n"
                f"- Pet ID: `{pet_info.get('id', 'N/A')}`\n"
                f"- Cấp độ: `{pet_info.get('level', 'N/A')}`\n"
                f"- Skin ID: `{pet_info.get('skinId', 'N/A')}`\n\n"

                f"🗨️ *Thông tin xã hội:*\n"
                f"- Ngôn ngữ: `{social_info.get('language', 'N/A')}`\n"
                f"- Chữ ký: `{social_info.get('signature', 'N/A')}`\n"
            )

            bot.reply_to(message, result, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Không tìm thấy thông tin tài khoản.")

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi gọi API: {e}")
    except ValueError:
        bot.reply_to(message, "Không thể đọc phản hồi từ API (có thể không phải JSON).")



@bot.message_handler(commands=['gai'])
def send_gai_image(message):
    api_url = "https://subhatde.id.vn/images/gai"

    # Send a "searching" message
    searching_message = bot.reply_to(message, "🔎 Đang tìm kiếm ảnh...")
    sent_messages.append(searching_message.message_id)  # Store the message ID

    try:
        # Request image data from the API
        response = requests.get(api_url)
        data = response.json()

        # Delete the "searching" message after getting the response
        try:
            bot.delete_message(searching_message.chat.id, searching_message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass  # Ignore if already deleted

        # Check if response contains an "url" field
        if 'url' in data:
            image_url = data['url']

            # Send the image to the user with a caption
            caption_text = f"Ảnh Mà Bạn Yêu Cầu, @{message.from_user.username}"
            sent_message = bot.send_photo(message.chat.id, image_url, caption=caption_text)
            sent_messages.append(sent_message.message_id)  # Store the message ID

            # Start a thread to delete all messages after 60 seconds
            threading.Thread(target=delete_all_messages_after_delay, args=(message.chat.id, 60)).start()
        else:
            bot.reply_to(message, "Không tìm thấy ảnh từ API.")
    except Exception as e:
        # Delete the "searching" message if an error occurs
        try:
            bot.delete_message(searching_message.chat.id, searching_message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass  # Ignore if already deleted
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}")

@bot.message_handler(commands=['vdanime'])
def send_random_anime_video(message):
    try:
        waiting_message = bot.reply_to(message, "Đang lấy video...⌛")

        # Lấy video từ API
        response = requests.get("https://apiquockhanh.click/video/videoanime", timeout=5)  # timeout để tránh chờ quá lâu
        data = response.json()

        if data and "url" in data:
            video_url = data["url"]
            bot.send_video(
                chat_id=message.chat.id,
                video=video_url,
                caption="🎬 Video anime ngẫu nhiên 🎥"
            )
        else:
            bot.send_message(message.chat.id, "Không thể lấy video anime ngẫu nhiên.")
        
        bot.delete_message(message.chat.id, waiting_message.message_id)
    
    except requests.Timeout:
        bot.send_message(message.chat.id, "Quá thời gian chờ API. Vui lòng thử lại.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra: {str(e)}")

# Hàm để xóa tất cả thông điệp sau một khoảng thời gian nhất định
def delete_all_messages_after_delay(chat_id, delay):
    time.sleep(delay)
    # Xóa các thông điệp đã gửi (thực hiện với các message_id đã lưu)
    for message_id in sent_messages:
        try:
            bot.delete_message(chat_id, message_id)
        except telebot.apihelper.ApiTelegramException:
            pass  # Không làm gì nếu thông điệp đã bị xóa hoặc không tồn tại


# Hàm xử lý lệnh /i4cap
@bot.message_handler(commands=['capcut'])
def i4cap(message):

    command_data = message.text.split()

    if len(command_data) != 2:
        bot.reply_to(message, "Vui lòng nhập link hợp lệ theo cú pháp:\n /i4cap [link]")
        return

    link = command_data[1]
    api_url = f"https://subhatde.id.vn/capcut/info?url={link}"
    searching_message = bot.reply_to(message, "🔎 Đang tìm kiếm thông tin...")

    try:
        response = requests.get(api_url)
        # Xóa thông điệp tìm kiếm
        bot.delete_message(searching_message.chat.id, searching_message.message_id)

        data = response.json()

        if 'user' in data:
            user_info = data['user']
            statistics = data['user_statistics']
            relation_info = user_info.get('relation_info', {}).get('statistics', {})

            name = user_info.get('name', 'Không có tên')
            avatar_url = user_info.get('avatar_url', '')
            followers = relation_info.get('follower_count', 'Không có thông tin')
            likes = statistics.get('like_count', 'Không có thông tin')

            message_text = f"🔎 @{message.from_user.username} đã yêu cầu thông tin cho link: {link}\n" \
                           f"👤 Tên: {name}\n" \
                           f"📊 Người theo dõi: {followers}\n" \
                           f"❤️ Lượt thích: {likes}"

            if avatar_url:
                sent_message = bot.send_photo(message.chat.id, avatar_url, caption=message_text)
            else:
                sent_message = bot.send_message(message.chat.id, message_text)

            sent_messages.append(sent_message.message_id)
            threading.Thread(target=delete_all_messages_after_delay, args=(message.chat.id, 60)).start()

        else:
            bot.reply_to(message, "Không tìm thấy thông tin cho link này.")
    except Exception as e:
        bot.delete_message(searching_message.chat.id, searching_message.message_id)
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}")

#sử lí reg acc fb 282
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = {
    'api_key': '882a8490361da98702bf97a021ddc14d',
    'secret': '62f8ce9f74b12f84c123cc23437a4a32'
}

email_prefix = [
    'gmail.com',
    'hotmail.com',
    'yahoo.com',
    'live.com',
    'rocket.com',
    'outlook.com',
]


def create_account_html():
  
    random_birth_day = datetime.strftime(datetime.fromtimestamp(random.randint(
        int(time.mktime(datetime.strptime('1980-01-01', '%Y-%m-%d').timetuple())),
        int(time.mktime(datetime.strptime('1995-12-30', '%Y-%m-%d').timetuple()))
    )), '%Y-%m-%d')

  
    names = {
        'first': ['JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'WILLIAM', 'DAVID'],
        'last': ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER'],
        'mid': ['Alexander', 'Anthony', 'Charles', 'Dash', 'David', 'Edward']
    }

   
    random_first_name = random.choice(names['first'])
    random_name = f"{random.choice(names['mid'])} {random.choice(names['last'])}"
    password = f'{random.randint(0, 9999999)}?#@'
    full_name = f"{random_first_name} {random_name}"
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()

 
    hash_ = f"{md5_time[0:8]}-{md5_time[8:12]}-{md5_time[12:16]}-{md5_time[16:20]}-{md5_time[20:32]}"
    email_rand = f"{full_name.replace(' ', '').lower()}{hashlib.md5((str(time.time()) + datetime.strftime(datetime.now(), '%Y%m%d')).encode()).hexdigest()[0:6]}@{random.choice(email_prefix)}"
    gender = 'M' if random.randint(0, 10) > 5 else 'F'

  
    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': random_birth_day,
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': random_first_name,
        'format': 'json',
        'gender': gender,
        'lastname': random_name,
        'email': email_rand,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': hash_,
        'return_multiple_errors': True
    }

    sig = ''.join([f'{k}={v}' for k, v in sorted(req.items())])
    ensig = hashlib.md5((sig + app['secret']).encode()).hexdigest()
    req['sig'] = ensig

    api = 'https://b-api.facebook.com/method/user.register'

    def _call(url='', params=None, post=True):
        headers = {
            'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
        }
        if post:
            response = requests.post(url, data=params, headers=headers, verify=False)
        else:
            response = requests.get(url, params=params, headers=headers, verify=False)
        return response.text

    reg = _call(api, req)
    reg_json = json.loads(reg)
    uid = reg_json.get('session_info', {}).get('uid')
    access_token = reg_json.get('session_info', {}).get('access_token')

 
    error_code = reg_json.get('error_code')
    error_msg = reg_json.get('error_msg')

    if uid is not None and access_token is not None:
       
        return f"""
        <blockquote expandable>
        <b>Birthday 🎂:</b> {random_birth_day}\n
        <b>Fullname ®️:</b> {full_name}\n
        <b>Email 📧 :</b> {email_rand}\n
        <b>Password 🔑:</b> {password}\n
        <b>UID 🆔:</b> {uid}\n
        <b>Token 🎧:</b> {access_token}\n
        </blockquote>
        """
    else:
        
        if error_code and error_msg:
            return f"""
            <b>Error Code:</b> {error_code}\n
            <b>Error Message:</b> {error_msg}\n
            """
        else:
            return "<b>Error:</b> Unknown error occurred. Please try again."


@bot.message_handler(commands=['regfb'])
def send_account_info(message):
    account_info_html = create_account_html()
    bot.send_message(message.chat.id, account_info_html, parse_mode="HTML")


@bot.message_handler(commands=['id'])
def get_user_id(message):
    # Kiểm tra xem tin nhắn có phải là trả lời một tin nhắn khác không
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>Vui lòng trả lời tin nhắn của người mà bạn muốn lấy ID.</blockquote>', parse_mode='HTML')
        return
    
    # Lấy ID của người dùng mà bạn đang trả lời
    user_id = message.reply_to_message.from_user.id
    username = message.reply_to_message.from_user.username or "Không có username"

    # Gửi ID của người dùng
    bot.reply_to(message, f'<blockquote>ID của người dùng: <b>{user_id}</b></blockquote>', parse_mode='HTML')


# Biến trạng thái để theo dõi việc khóa chat
@bot.message_handler(commands=['lock'])
def lock_chat(message):
    user_id = message.from_user.id
    
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    # Tắt quyền gửi tin nhắn cho tất cả thành viên
    bot.set_chat_permissions(message.chat.id, telebot.types.ChatPermissions(can_send_messages=False))
    bot.send_message(message.chat.id, "✅ Chat đã bị khóa. Không ai có thể gửi tin nhắn.")

@bot.message_handler(commands=['unlock'])
def unlock_chat(message):
    user_id = message.from_user.id
    
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    # Mở lại quyền gửi tin nhắn cho tất cả thành viên
    bot.set_chat_permissions(message.chat.id, telebot.types.ChatPermissions(can_send_messages=True))
    bot.send_message(message.chat.id, "✅ Chat đã được mở. Tất cả mọi người có thể gửi tin nhắn.")


#chào mừng 
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        # Lấy tên người dùng mới (username) hoặc tên hiển thị (first name)
        username = new_member.username
        first_name = new_member.first_name
        
        # Tạo thông điệp chào mừng
        if username:
            user_info = f"@{username}"
        else:
            user_info = first_name
        
        # Nội dung tin nhắn chào mừng với thẻ <pre>
        welcome_text = f'''
<blockquote> 🎉 Chào mừng {user_info} đến với nhóm! 🎉
Hy vọng bạn sẽ có khoảng thời gian vui vẻ ở đây!
Nhập /help để xem danh sách lệnh !!!
</blockquote>
<blockquote> Mua /spamvip /vip Inbox Telegram: @ngotk999
</blockquote>
        '''
        
        # Gửi tin nhắn chào mừng
        bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

MOCK_API_URL = 'https://mockapi.io/projects/YOUR_PROJECT_ID/users/'

def check_facebook_info_mock(user_id):
    url = f"{MOCK_API_URL}{user_id}"
    
    try:
        response = requests.get(url)
        
        # Kiểm tra mã trạng thái HTTP
        if response.status_code != 200:
            return f"Lỗi khi truy cập API. Mã lỗi: {response.status_code}"
        
        # Kiểm tra phản hồi rỗng
        if not response.text:
            return "Phản hồi rỗng từ API."

        # In nội dung phản hồi để kiểm tra
        print("Phản hồi từ API:", response.text)

        # Kiểm tra xem phản hồi có phải JSON không
        try:
            data = response.json()
        except ValueError:
            return "Phản hồi từ API không phải JSON hợp lệ."
        
        # Xử lý và trả về kết quả nếu có dữ liệu JSON
        result = f"Name: {data.get('name', 'Không có')}\n" \
                 f"Location: {data.get('location', 'Không có')}\n" \
                 f"Gender: {data.get('gender', 'Không có')}\n" \
                 f"Friends Count: {data.get('friends_count', 'Không có')}"
        return result

    except Exception as e:
        return f"Lỗi: {str(e)}"




# Lắng nghe các tin nhắn khác
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Kiểm tra và xử lý các tin nhắn khác nếu cần
    pass


    
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id)
def continue_gemini_conversation(message):
    user_id = message.from_user.id
    # Lấy nội dung tin nhắn reply
    input_text = message.text.strip()
    # Thêm tin nhắn của người dùng vào lịch sử cuộc trò chuyện
    conversation_history[user_id].append({"role": "user", "content": input_text})
    # Gọi API và trả lời người dùng
    send_to_gemini_api(message, user_id, input_text)
def send_to_gemini_api(message, user_id, input_text):
    # Tạo payload JSON với lịch sử cuộc trò chuyện
    payload = {
        "contents": [
            {
                "parts": [{"text": msg["content"]} for msg in conversation_history[user_id]]  # Lưu tất cả tin nhắn trong cuộc hội thoại
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        # Gửi yêu cầu POST tới API Gemini
        response = requests.post(f'{BASE_URL}?key={API_KEY}', headers=headers, json=payload)
        # Kiểm tra và xử lý phản hồi
        if response.status_code == 200:
            data = response.json()
            # Trích xuất phần text của model từ phản hồi
            text_response = data['candidates'][0]['content']['parts'][0]['text']
            # Trả lời người dùng và giữ lại cuộc hội thoại
            sent_message = bot.reply_to(message, f"{text_response}")
            # Thêm câu trả lời của model vào lịch sử
            conversation_history[user_id].append({"role": "model", "content": text_response})
        else:
            error_message = response.json().get('error', {}).get('message', 'Không thể lấy dữ liệu.')
            bot.reply_to(message, f"Lỗi: {error_message}")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Có lỗi xảy ra khi kết nối API: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Lỗi không xác định: {str(e)}")
bot.infinity_polling(timeout=60, long_polling_timeout = 1)


import time

# Dictionary to track user message timestamps
user_messages = {}

# Mute duration in seconds (4 minutes)
MUTE_DURATION = 240

# Maximum messages allowed within the spam detection window (30 seconds)
MAX_MESSAGES = 15

# Function to filter messages, delete spams and mute spammers
@bot.message_handler(func=lambda message: True)
def filter_and_mute(message):
    user_id = message.from_user.id
    current_time = time.time()

    # Initialize user message tracking if the user is new
    if user_id not in user_messages:
        user_messages[user_id] = []

    # Remove messages older than the spam detection window (30 seconds) from the tracking list
    user_messages[user_id] = [msg_time for msg_time in user_messages[user_id] if current_time - msg_time < 30]

    # Add the current message timestamp
    user_messages[user_id].append(current_time)

    # Check if the user has sent more than MAX_MESSAGES in the last 30 seconds
    if len(user_messages[user_id]) > MAX_MESSAGES:
        try:
            # Mute the user for MUTE_DURATION (4 minutes)
            bot.restrict_chat_member(
                message.chat.id,
                user_id,
                can_send_messages=False
            )

            # Notify the user that they have been muted
            bot.reply_to(message, f"🚫 Bạn đã bị tạm thời cấm gửi tin nhắn trong {MUTE_DURATION // 60} phút vì gửi quá nhiều tin nhắn.")

            # Set a timer to unmute the user after MUTE_DURATION seconds (4 minutes)
            time.sleep(MUTE_DURATION)

            # Unmute the user after the mute duration
            bot.restrict_chat_member(
                message.chat.id,
                user_id,
                can_send_messages=True
            )
            # Notify the user that the mute has been lifted
            bot.send_message(message.chat.id, f"⏰ Bạn đã được mở lại quyền gửi tin nhắn.")
        except Exception as e:
            bot.reply_to(message, "Không thể tạm thời cấm người dùng.")

        # Delete the spam message as soon as it's detected
        bot.delete_message(message.chat.id, message.message_id)

    # Optional: If you want to filter banned words (you can add the BANNED_WORDS list if needed)
    # message_text = message.text.lower()
    # for banned_word in BANNED_WORDS:
    #     if banned_word in message_text:
    #         bot.delete_message(message.chat.id, message.message_id)
    #         bot.reply_to(message, "⚠️ Cảnh báo: Tin nhắn của bạn chứa từ ngữ không phù hợp.")
    #         break  # Stop after the first banned word is found
