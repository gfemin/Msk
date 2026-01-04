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
    '1696442023',    # User 2
    '',     # User 3
    ''      # User 4
]

# ==========================================
# 🎨 UI HELPER FUNCTION (ADDED 3DS)
# ==========================================
def get_dashboard_ui(total, current, live, die, ccn, low, cvv, threeds, last_cc, last_response):
    # Percentage Calculation
    percent = int((current / total) * 100) if total > 0 else 0
    
    # CC Privacy
    if len(last_cc) < 10:
        display_cc = "Wait..."
    else:
        display_cc = last_cc

    # Response Shortener
    if len(last_response) > 40:
        display_response = last_response[:40] + "..."
    else:
        display_response = last_response

    # The Design (Balanced 2x3 Layout)
    line = "━━━━━━━━━━━━━━━━━━"
    
    text = (
        f"{line}\n"
        f"• <b>RUSISVIRUS | VIP 🇲🇲</b>\n"
        f"{line}\n"
        f"• <code>{display_cc}</code>\n"
        f"• <b>Result:</b> {display_response}\n"
        f"• <b>Stripe Charge ($0.5)</b>\n"
        f"{line}\n"
        f"• <b>Hits:</b> {live}    • <b>Dead:</b> {die}\n"
        f"• <b>CVV:</b>  {cvv}    • <b>CCN:</b>  {ccn}\n"
        f"• <b>Low:</b>   {low}    • <b>3Ds:</b>   {threeds}\n" 
        f"{line}\n"
        f"• <b>Processing...</b> {percent}%"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⛔ STOP", callback_data="stop"))
    
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
# 🚀 CHECKER LOGIC
# ==========================================
def run_checker(message):
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    threeds = 0  # <--- New 3Ds Counter Added
    
    chat_id = message.chat.id
    
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
            
            # Initial UI
            view_text, markup = get_dashboard_ui(total, 0, 0, 0, 0, 0, 0, 0, "Wait...", "Starting...")
            bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)

            for index, cc in enumerate(lino, 1):
                cc = cc.strip()
                
                # STOP Check
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>STOPPED (User Request)</b>')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return

                # BIN Lookup
                try:
                    data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                except:
                    data = {}
                
                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '')
                bank = data.get('bank', 'Unknown')
                
                # STOP Check 2
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='🛑 <b>STOPPED (User Request)</b>')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return

                start_time = time.time()
                
                # Gate Check
                try:
                    last = str(func_timeout(100, Tele, args=(cc,)))
                except FunctionTimedOut:
                    last = 'Gateway Time Out ❌'
                except Exception as e:
                    print(e)
                    last = 'System Error ⚠️'
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                is_hit = 'Payment Successful!' in last or 'funds' in last or 'security code' in last or 'Your card does not support' in last or 'completion' in last
                
                # Update UI
                if is_hit or (index == 1) or (index % 8 == 0) or (index == total):
                    view_text, markup = get_dashboard_ui(total, index, ch, dd, ccn, lowfund, cvv, threeds, cc, last)
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except Exception as e:
                        pass 
                
                print(f"{chat_id} : {cc} -> {last}")
                
                if 'Payment Successful!' in last or 'funds' in last:
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - {last} - {bank} ({country})\n")

                # ==========================================
                # 🔥 RESULT MESSAGES
                # ==========================================
                line = "━━━━━━━━━━━━━━━━━━"
                
                if 'Payment Successful!' in last:
                    ch += 1
                    msg = f'''{line}
• <code>{cc}</code>
• <b>Result:</b> PAYMENT SUCCESSFUL! ✅
{line}
• <b>Bin:</b> {brand} - {card_type}
• <b>Bank:</b> {bank}
• <b>Country:</b> {country} - {country_flag}
• <b>Time:</b> {execution_time:.1f} sec
{line}
<b>Bot by: @Rusisvirus</b>'''
                    bot.reply_to(message, msg)
                    
                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1
                    msg = f'''{line}
• <code>{cc}</code>
• <b>Result:</b> CVV MATCH ✅
{line}
• <b>Bin:</b> {brand} - {card_type}
• <b>Bank:</b> {bank}
• <b>Country:</b> {country} - {country_flag}
• <b>Time:</b> {execution_time:.1f} sec
{line}
<b>Bot by: @Rusisvirus</b>'''
                    bot.reply_to(message, msg)
                
                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1
                    msg = f'''{line}
• <code>{cc}</code>
• <b>Result:</b> CCN LIVE ✅
{line}
• <b>Bin:</b> {brand} - {card_type}
• <b>Bank:</b> {bank}
• <b>Country:</b> {country} - {country_flag}
• <b>Time:</b> {execution_time:.1f} sec
{line}
<b>Bot by: @Rusisvirus</b>'''
                    bot.reply_to(message, msg)
                    
                    # Update UI immediately for Hits
                    view_text, markup = get_dashboard_ui(total, index, ch, dd, ccn, lowfund, cvv, threeds, cc, last)
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                    except:
                        pass
                    
                elif 'funds' in last:
                    lowfund += 1
                    msg = f'''{line}
• <code>{cc}</code>
• <b>Result:</b> INSUFFICIENT FUNDS! 🚫
{line}
• <b>Bin:</b> {brand} - {card_type}
• <b>Bank:</b> {bank}
• <b>Country:</b> {country} - {country_flag}
• <b>Time:</b> {execution_time:.1f} sec
{line}
<b>Bot by: @Rusisvirus</b>'''
                    bot.reply_to(message, msg)
                    
                elif 'The payment needs additional action before completion!' in last:
                    threeds += 1  # <--- Increment 3Ds Counter
                    msg = f'''{line}
• <code>{cc}</code>
• <b>Result:</b> 3D ACTION REQUIRED ⚠️
{line}
• <b>Bin:</b> {brand} - {card_type}
• <b>Bank:</b> {bank}
• <b>Country:</b> {country} - {country_flag}
• <b>Time:</b> {execution_time:.1f} sec
{line}
<b>Bot by: @Rusisvirus</b>'''
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
print("🤖 Bot Started (Added 3Ds Support)...")
while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
