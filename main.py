import requests
import telebot, time, threading
from telebot import types
from gatet import Tele
import os
from func_timeout import func_timeout, FunctionTimedOut

token = '8299646020:AAHM7qDFRuBjcMRwFiLMwXMWxXxNs8mk0G4'
bot = telebot.TeleBot(token, parse_mode="HTML")

# ==========================================
# 👇 ALLOWED USERS LIST
ALLOWED_IDS = [
    '1915369904',    # Owner
    '',     # User 2
    '',     # User 3
    ''      # User 4
]
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) not in ALLOWED_IDS:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return
    bot.reply_to(message, "𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐟𝐢𝐥𝐞 𝐧𝐨𝐰❤️")

# 🔥 NEW FEATURE: Download Lives File 🔥
@bot.message_handler(commands=["getlives"])
def get_lives(message):
    if str(message.chat.id) not in ALLOWED_IDS: return
    
    try:
        if os.path.exists("lives.txt"):
            with open("lives.txt", "rb") as f:
                bot.send_document(message.chat.id, f, caption="✅ <b>Here are your Charged/Live Cards</b>", parse_mode="HTML")
        else:
            bot.reply_to(message, "No Live cards saved yet! ❌")
    except Exception as e:
        bot.reply_to(message, f"Error sending file: {e}")

# 🔥 NEW FEATURE: Clear Lives File 🔥
@bot.message_handler(commands=["clearlives"])
def clear_lives(message):
    if str(message.chat.id) not in ALLOWED_IDS: return
    
    if os.path.exists("lives.txt"):
        os.remove("lives.txt")
        bot.reply_to(message, "🗑️ <b>lives.txt has been cleared!</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, "File is already empty.")

@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) not in ALLOWED_IDS:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return

    # Threading စတင်ခြင်း
    t = threading.Thread(target=run_checker, args=(message,))
    t.start()

def run_checker(message):
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    chat_id = message.chat.id
    
    # NAME CONFLICT FIX
    file_name = f"combo_{chat_id}_{int(time.time())}.txt"
    stop_file = f"stop_{chat_id}.stop"

    try:
        ko = bot.reply_to(message, "𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐍𝐨𝐰! 🚀").message_id
        ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
        
        with open(file_name, "wb") as w:
            w.write(ee)
            
        with open(file_name, 'r') as file:
            lino = file.readlines()
            total = len(lino)
            
            for cc in lino:
                cc = cc.strip()
                
                # ===== STOP CHECK (1) : အစမှာတစ်ခေါက်စစ်မယ် =====
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>STOPPED (User Request)</b>')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return
                
                # ===== BIN LOOKUP =====
                try:
                    data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                except:
                    data = {}
                
                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '')
                bank = data.get('bank', 'Unknown')
                
                # ===== STOP CHECK (2) : BIN ရှာပြီးရင် ထပ်စစ်မယ် (ပိုမြန်အောင်လို့) 🔥 =====
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>STOPPED (User Request)</b>')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return

                start_time = time.time()
                
                # ===== CHECKER WITH TIMEOUT =====
                try:
                    # 25 seconds timeout
                    last = str(func_timeout(70, Tele, args=(cc,)))
                except FunctionTimedOut:
                    last = 'Gateway Time Out ❌'
                except Exception as e:
                    print(e)
                    last = 'Error'
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # ===== DASHBOARD VIEW =====
                view_text = f"""\
• <code>{cc}</code>

🟢 sᴛᴀᴛᴜs  ➜ <code>{last}</code>

💳 ᴄʜᴀʀɢᴇᴅ  ➜ <code>[ {ch} ]</code>

🔐 ᴄᴄɴ ➜ <code>[ {ccn} ]</code>

🔐 ᴄᴠᴠ ➜ <code>[ {cvv} ]</code>

⚠️ ʟᴏᴡ ғᴜɴᴅs ➜ <code>[ {lowfund} ]</code>

📊 ᴅᴇᴄʟɪɴᴇᴅ ➜ <code>[ {dd} ]</code>

• ᴛᴏᴛᴀʟ ➜ <code>[ {total} ]</code>
"""
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton("⛔ sᴛᴏᴘ ⚠️", callback_data="stop"))
                
                is_hit = 'successful' in last or 'funds' in last or 'security code' in last
                
                if is_hit or (dd % 10 == 0):
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except Exception as e:
                        pass 
                
                # ===== HIT SENDER & SAVER =====
                print(f"{chat_id} : {cc} -> {last}")
                
                # 🔥 SAVE TO FILE LOGIC 🔥
                if 'successful' in last or 'funds' in last:
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - {last} - {bank} ({country})\n")

                if 'successful' in last:
                    ch += 1
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹 ✅</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                # 🔥 CVV MESSAGE ADDED 🔥
                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝐂𝐕𝐕 𝐌𝐢𝐬𝐦𝐚𝐭𝐜𝐡 ⚠️</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                
                # 🔥 CCN MESSAGE ADDED 🔥
                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝐂𝐂𝐍 𝐋𝐢𝐯𝐞 ✅</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except:
                        pass
                    
                elif 'funds' in last:
                    lowfund += 1
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝗜𝗻𝘀𝘂𝗳𝗳𝗶𝗰𝗶𝗲𝗻𝘁 𝗙𝘂𝗻𝗱𝘀 ⛔</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                elif 'The payment needs additional action before completion!' in last:
                    cvv += 1
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝟑𝗗 𝗿𝗲𝗾𝘂𝗶𝗿𝗲𝘀_𝗮𝗰𝘁𝗶𝗼𝗻 ⚠️</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                        
                else:
                    dd += 1
                    time.sleep(1)
        
        # Cleanup input file only
        if os.path.exists(file_name): os.remove(file_name)
        bot.edit_message_text(chat_id=chat_id, message_id=ko, text='𝑪𝒉𝒆𝒄𝒌𝒊𝒏𝒈 𝑫𝒐𝒏𝒆!\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus')

    except Exception as e:
        print(f"Error for {chat_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    stop_file = f"stop_{call.message.chat.id}.stop"
    with open(stop_file, "w") as file:
        pass
    bot.answer_callback_query(call.id, "Stopping...")

# ===== SAFE POLLING =====
import telebot.apihelper as apihelper
apihelper.REQUEST_TIMEOUT = 30

while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
