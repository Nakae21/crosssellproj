import requests

PAYSTACK_SECRET_KEY = 'sk_test_09fbe149b20525947cb57fc6ac887d6d68868eb8'   # Replace with your secret key
PAYSTACK_PUBLIC_KEY = 'pk_test_cb990422d3bc705e77576b519a6fca3d6d72581d'   # Replace with your public key


def verify_payment(reference):
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    return response.json()
