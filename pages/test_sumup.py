import streamlit as st
from sumup_oauthsession import OAuth2Session
import requests
import json
import string
import random
import streamlit.components.v1 as components
from datetime import datetime

def display_transaction_details(transaction_data):
    # Parsing the transaction data
    transaction_id = transaction_data.get("id", "N/A")
    amount = transaction_data.get("amount", "N/A")
    currency = transaction_data.get("currency", "N/A")
    payment_type = transaction_data.get("payment_type", "N/A")
    status = transaction_data.get("status", "N/A")
    timestamp = transaction_data.get("timestamp", "N/A")
    local_time = transaction_data.get("local_time", "N/A")
    card_type = transaction_data.get("card", {}).get("type", "N/A")
    card_last_4_digits = transaction_data.get("card", {}).get("last_4_digits", "N/A")
    product_summary = transaction_data.get("product_summary", "N/A")
    products = transaction_data.get("products", [])
    receipt_url = next((link["href"] for link in transaction_data.get("links", []) if link["rel"] == "receipt" and link["type"] == "image/png"), "N/A")

    # Convert timestamps to human-readable format
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
    local_time = datetime.strptime(local_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S %Z")

    # Displaying the important information
    st.write(f"Transaction ID: {transaction_id}")
    st.write(f"Amount: {amount} {currency}")
    st.write(f"Status: {status}")
    st.write(f"Payment Type: {payment_type}")
    st.write(f"Timestamp (UTC): {timestamp}")
    st.write(f"Local Time: {local_time}")
    st.write(f"Card Type: {card_type} (Last 4 digits: {card_last_4_digits})")
    st.write(f"Product Summary: {product_summary}")
    st.write(f"Receipt URL (PNG): {receipt_url}")

    st.write("\nProducts:")
    for product in products:
        name = product.get("name", "N/A")
        price = product.get("price", "N/A")
        quantity = product.get("quantity", "N/A")
        total_price = product.get("total_price", "N/A")
        st.write(f" - {name}: {quantity} x {price} = {total_price} {currency}")

def generate_checkout_reference(length=6):
    # Define the characters to choose from for the random string
    characters = string.ascii_uppercase + string.digits

    # Generate a random short string of the specified length
    checkout_reference = ''.join(random.choice(characters) for _ in range(length))

    return checkout_reference

def get_sumup_token():
    # Define the SumUp token endpoint URL
    token_url = 'https://api.sumup.com/token'

    # Define the payload for the POST request
    payload = {
        'grant_type': 'client_credentials',
        'client_id': st.secrets["sumup"]["CLIENT_ID"],
        'client_secret': st.secrets["sumup"]["CLIENT_SECRET"]
    }

    # Make an HTTP POST request to the SumUp token endpoint
    response = requests.post(token_url, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the access token from the response
        access_token = response.json().get('access_token')
        st.success(f'Success! Access token: {access_token}')

        pretty_json = json.dumps(response.json(), indent=4)
        st.json(pretty_json, expanded=False)
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')

    return access_token

def create_sumup_checkout(reference, amount, currency, email, description):
    # Define the SumUp checkout endpoint URL
    checkout_url = 'https://api.sumup.com/v0.1/checkouts'

    # Define the headers for the API request
    # headers = {
    #     'Authorization': f'Bearer  {st.secrets["sumup"]["CLIENT_API_SECRET"]}',
    #     'Content-Type': 'application/json'
    # }
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }

    # Define the payload for the API request
    payload = {
        'checkout_reference': reference,
        'amount': amount,
        'currency': currency,
        'pay_to_email': email,
        'description': description,
        'merchant_code': st.secrets["sumup"]["MERCHANT_ID"],

    }

    # Make an HTTP POST request to the SumUp checkout endpoint
    response = requests.post(checkout_url, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the checkout ID from the response
        checkout_id = response.json().get('id')
        st.success(f'Success! Checkout ID: {checkout_id}')
    else:
        # Display an error message if the request failed
        st.write(response)
        st.warning(f'Error: {response.text}')

def get_checkout(checkout_id):
    # Define the API endpoint URL
    url = f"https://api.sumup.com/v0.1/checkouts/{checkout_id}"

    # Get the SumUp API key from Streamlit secrets

    # Set up the request headers with the API key
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }

    # Send a GET request to retrieve the checkout
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code in [200, 201, 202, 204]:
        # Parse the JSON response
        checkout_data = response.json()
        return checkout_data
    else:
        st.error(f"Error retrieving checkout: {response.status_code} - {response.text}")

def process_checkout(checkout_id, payment_data):
    # Define the API endpoint URL
    url = f"https://api.sumup.com/v0.1/checkouts/{checkout_id}"

    # Get the SumUp API key from Streamlit secrets

    # Set up the request headers with the API key
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }
    # Send a POST request to process the checkout
    response = requests.put(url, json=payment_data, headers=headers)

    # Check if the request was successful
    if response.status_code in [200, 201, 202, 204]:
        st.write(response.status_code)
        st.write(response.json())
        st.success("Checkout processed successfully")
        return response.json()
    else:
        st.error(f"Error processing checkout: {response.status_code} - {response.text}")

def get_sumup_payment_methods(merchant_id, amount, currency):
    # Define the SumUp payment methods endpoint URL
    payment_methods_url = f'https://api.sumup.com/v0.1/merchants/{merchant_id}/payment-methods'
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }
    # Define the query parameters for the API request
    params = {
        # 'amount': amount,
        # 'currency': currency
    }
    st.toast(merchant_id)
    # Make an HTTP GET request to the SumUp payment methods endpoint
    response = requests.get(payment_methods_url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the payment methods from the response
        payment_methods = response.json()
        st.write('Available Payment Methods:')
        st.write(response.json())
        for method in payment_methods:
            st.write(method)
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')

def get_sumup_transaction_history(num_transactions):
    # Define the SumUp transaction history endpoint URL
    transaction_history_url = 'https://api.sumup.com/v0.1/me/transactions/history'

    # Define the query parameters for the API request
    params = {
        'limit': 100,
        'order': 'descending',
        'statuses[]': 'SUCCESSFUL',
        'types[]': 'PAYMENT', 
        # 'changes_since': '2017-10-23T08:23:00.000Z'
    }

    params = {
        'limit': num_transactions,
        'order': 'descending',
        # 'statuses[]': 'SUCCESSFUL',
        'types[]': 'PAYMENT', 
        # 'changes_since': '2017-10-23T08:23:00.000Z'
    }

    # Define the request headers with the access token
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }

    # Make an HTTP GET request to the SumUp transaction history endpoint
    response = requests.get(transaction_history_url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # st.write(response.json())
        # Extract the transaction history from the response
        transaction_history = response.json()
        # st.write('Transaction History:')
        return transaction_history
        # for transaction in transaction_history:
            # st.write(transaction)
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')

def get_sumup_accounts():
    # Define the SumUp accounts endpoint URL
    accounts_url = 'https://api.sumup.com/v0.1/me/accounts'

    # Define the request headers with the client API secret from Streamlit secrets
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }

    # Make an HTTP GET request to the SumUp accounts endpoint
    response = requests.get(accounts_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the accounts data from the response
        accounts_data = response.json()
        st.write('SumUp Accounts:')
        for account in accounts_data:
            st.write(account)
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')
     
def get_transaction_details(tx_id):
    # Define the SumUp transaction details endpoint URL
    api_endpoint = f'https://api.sumup.com/v0.1/me/transactions'

    # Define the request headers with the client API secret from Streamlit secrets
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }
    params = {
        'id': tx_id
    }
    # Make an HTTP GET request to the SumUp transaction details endpoint
    response = requests.get(api_endpoint, headers=headers, data=params)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the transaction details from the response
        transaction_details = response.json()
        st.write('Transaction Details:')
        st.json(transaction_details, expanded=False)
        return transaction_details
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')
        return None
   
def main():


    src_101 = "https://pay.sumup.com/b2c/QDJLWO13"
    src_100K = 'https://pay.sumup.com/b2c/Q8F8EX3C'
    src_free = "https://pay.sumup.com/b2c/Q2RYJEC8"
    src_bet = 'https://pay.sumup.com/b2c/QDEYTAA2'

    st.write(st.secrets["sumup"])

    redirect_uri = "https://individual-choice.streamlit.app/"
    base_url = "https://api.sumup.com/"

    sumup = OAuth2Session(
        base_url=base_url,
        client_id=st.secrets["sumup"]["CLIENT_ID"],
        client_secret=st.secrets["sumup"]["CLIENT_SECRET"],
        redirect_uri=redirect_uri,
    )

    st.write(sumup)
    st.write(sumup.authorization_url())
    st.write(sumup.state)
    # sumup.authorize()

    # Define the SumUp API endpoint URL
    api_url = 'https://api.sumup.com/v0.1/me'

    # Define the authorization header with your SumUp API token
    headers = {
        'Authorization': f'Bearer {st.secrets["sumup"]["CLIENT_API_SECRET"]}'
    }

    # Make an HTTP GET request to the SumUp API endpoint
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Display the response data
        st.toast('Success! Response received from SumUp API')
        st.success(f'Response: {response.json()}')
        pretty_json = json.dumps(response.json(), indent=4)
        st.json(pretty_json, expanded=False)
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')

    if st.button('Generate SumUp Token'):
        get_sumup_token()


    st.title('SumUp Checkout Creator')

    # Input fields for the checkout parameters
    reference = st.text_input('Checkout Reference', value=generate_checkout_reference(6))
    amount = st.number_input('Amount', value=10.0, step=0.01)
    currency = st.text_input('Currency', value='EUR')
    email = st.text_input('Pay To Email', value = 'test@sumup.com')
    description = st.text_input('Description')

    # Display a button to create the SumUp checkout
    if st.button('Create SumUp Checkout'):
        # Pass the input values to the function to create the checkout
        create_sumup_checkout(reference, amount, currency, email, description)
        
    checkout_id = st.text_input('Checkout ID')
    
    st.title('SumUp Checkout Retriever')
    
    checkout_data = get_checkout(checkout_id)
    if checkout_data:
        st.write("Checkout Data:")
        st.write(checkout_data)
        
    st.title('SumUp Payment Methods')

    st.title('SumUp Checkout Executor')

    card_data = {
        "payment_type": "card",
        "card": {
            "cvv": "2611",
            "expiry_month": "09",
            "expiry_year": "2025",
            "last_4_digits": "2611",
            "name": "A LEON BALDELLI",
            "number": "4971601396773204",
            "type": "VISA"
        }
    }
    st.write(card_data)
    checkout = None
    if st.button('Process Checkout'):
        checkout = process_checkout(checkout_id, card_data)

    if checkout:
        # Extract POST method, URL, and payload data from the response
        post_method = checkout["next_step"]["method"]
        post_url = checkout["next_step"]["url"]
        payload_data = checkout["next_step"]["payload"]

        # Make a POST request
        response = requests.post(post_url, data=payload_data)

        # Check if the request was successful
        if response.status_code == 200:
            st.success("POST request successful")
        else:
            st.error(f"POST request failed with status code: {response.status_code}")        
        st.write(response)
        st.write(response.content)
        # st.write(response.text)
        
        st.components.v1.iframe(response.text, height=600)
        st.write(response.text, unsafe_allow_html=True)
               
    # Get the merchant ID from Streamlit secrets
    merchant_id = st.secrets["sumup"]['MERCHANT_ID']

    # Input fields for the amount and currency
    amount = st.number_input('Amount', value=9.99, step=0.01)
    currency = st.text_input('Currency', value='EUR', key='currency')

    # Display a button to retrieve the payment methods
    if st.button('Retrieve Payment Methods'):
        # Call the function to get the payment methods
        get_sumup_payment_methods(merchant_id, amount, currency)

    st.title('SumUp Transaction History')

    # Input field for the SumUp access token
    num_transactions = st.number_input('Transaction limits', value=3, step=1)

    # Display a button to retrieve the transaction history
    if st.button('Retrieve Transaction History'):
        # Call the function to get the transaction history
        tx_history = get_sumup_transaction_history(num_transactions)
        if tx_history:
            st.write("Transaction History")
            st.write(tx_history["items"][0].keys())
            transaction_rows = []

            for transaction in tx_history["items"]:
                            
                row = {
                    "Timestamp": transaction["timestamp"],
                    "Transaction Code": transaction["transaction_code"],
                    "Amount": transaction["amount"],
                    "Currency": transaction["currency"],
                    "Status": transaction["status"],
                    "Card Type": transaction["card_type"],
                    "Payment Type": transaction["payment_type"],
                    "Transaction ID": transaction["transaction_id"],
                }
                transaction_rows.append(row)

            st.table(transaction_rows)

    st.title('Transaction Details')
    tx_id = st.text_input('Transaction ID')

    if st.button('Retrieve Transaction Details'):
        tx_data = get_transaction_details(tx_id)
        
        display_transaction_details(tx_data)
        
    st.title('SumUp Accounts')

    # Display a button to retrieve the SumUp accounts
    if st.button('Retrieve SumUp Accounts'):
        # Call the function to get the SumUp accounts
        get_sumup_accounts()

    st.title('SumUp widget')
    
    @st.dialog('SumUp Checkout Creator')
    def sumup_pay(src):
        components.iframe(src, height=500)

    st.button('SumUp Pay', on_click=sumup_pay, args=(src_101,))
    
    


if __name__ == '__main__':
    main()