import requests
from requests.auth import HTTPBasicAuth

my_domain = "https://wandabi.pythonanywhere.com/"
environment = "sandbox"


def register_url(consumer_key, consumer_secret, account_id, shortcode):
    confirmation_url = f'{my_domain}transaction/{account_id}/'
    validation_url = f'{my_domain}validation/{account_id}/'

    # Generate access token
    auth_url = f'https://{environment}.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code != 200:
        print("Failed to get access token:", response.status_code, response.text)
        return {"error": "Failed to get access token"}

    access_token = response.get('access_token')
    print("Access Token:", access_token)

    if not access_token:
        print("Access token is None. Check credentials.")
        return {"error": "Access token not retrieved"}

    # Register URLs for C2B
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    register_url_endpoint = f'https://{environment}.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    request_data = {
        "ShortCode": shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": confirmation_url,
        "ValidationURL": validation_url
    }

    try:
        response = requests.post(register_url_endpoint, json=request_data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully registered URL:", response.json())
        else:
            print("Failed to register URL:", response.status_code, response.text)
            return {"error": f"Failed to register URL. Status code: {response.status_code}"}

    except Exception as e:
        print("Exception occurred:", e)
        return {"error": str(e)}

    return response.json()
