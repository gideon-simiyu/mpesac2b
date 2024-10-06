import requests
import base64
from requests.auth import HTTPBasicAuth

my_domain = "https://yourdomain.com/"
environment = "sandbox"

def register_url(consumer_key, consumer_secret, account_id, shortcode):
    confirmation_url = f'{my_domain}confirmation/{account_id}/'  # URL for transaction confirmations
    validation_url = f'{my_domain}validation/{account_id}/'
    
    # Generate access token
    auth_url = f'https://{environment}.safaricom.co.ke/oauth/v2/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = response.json().get('access_token')
    
    # Register URLs for C2B
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    register_url_endpoint = f'https://{environment}.safaricom.co.ke/mpesa/c2b/v2/registerurl'
    request_data = {
        "ShortCode": shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": confirmation_url,
        "ValidationURL": validation_url
    }
    
    response = requests.post(register_url_endpoint, json=request_data, headers=headers)
    
    return response.json()
