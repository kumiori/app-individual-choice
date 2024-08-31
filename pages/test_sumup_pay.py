import streamlit as st
import requests
from sumup_oauthsession import OAuth2Session
from pages.test_sumup import generate_checkout_reference
import json
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript as stjs


# Replace with your SumUp API credentials
API_BASE_URL = 'https://api.sumup.com/v0.1'
ACCESS_TOKEN = st.secrets["sumup"]["CLIENT_API_SECRET"]
base_url = "https://api.sumup.com/"
redirect_uri = "https://individual-choice.streamlit.app/"

# initialise the sumup object in session state
if 'sumup' not in st.session_state:
    st.session_state['sumup'] = None

if 'checkouts' not in st.session_state:
    st.session_state['checkouts'] = []


def authenticate():
    """Authenticate with the SumUp API."""
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    return headers

def create_sumup_checkout(reference, amount, currency, email, description):
    # Define the SumUp checkout endpoint URL
    checkout_url = f'{API_BASE_URL}/checkouts'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
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
        st.session_state['checkouts'].append(checkout_id)
        
        return response.json()
    else:
        # Display an error message if the request failed
        st.write(response)
        st.warning(f'Error: {response.text}')
        return None

def connect_me():
    url = f'{API_BASE_URL}/me'
    headers = authenticate()

    response = requests.get(url, headers=headers)
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

def get_sumup_token(sumup):
    return sumup.token

def get_checkout_info(checkout_id):
    url = f'{API_BASE_URL}/checkouts/{checkout_id}'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    # Define the payload for the API request
    payload = {}

    # Make an HTTP POST request to the SumUp checkout endpoint
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the checkout ID from the response
        checkout_id = response.json().get('id')
        st.success(f'Success! Checkout info retrieved')
        
        return response.json()
    else:
        # Display an error message if the request failed
        st.write(response)
        st.warning(f'Error: {response.text}')
        return None

def list_checkouts():
    url = f'{API_BASE_URL}/checkouts'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

def process_checkout(checkout_id):
    url = f'{API_BASE_URL}/checkouts/{checkout_id}'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    payload = {'payment_type': 'card'}

    response = requests.put(url, headers=headers, json=payload)
    if response.status_code in [200, 201, 202, 204]:
        # Extract the checkout ID from the response
        st.success(f'Success! Checkout processing...')
        return response.json()
    else:
        # Display an error message if the request failed
        st.write(response)
        st.warning(f'Error: {response.text}')
        return None

@st.dialog("This is a dialogue")
def sumup_widget(checkout_id):
        # st.markdown("""
        #     <script src="https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js"></script>
        #     <script>
        #         function initSumUpWidget() {
        #             // Check if SumUpCard is available
        #             console.log('initialising SumUpCard.');
        #             if (window.SumUpCard) {
        #                 // Example of mounting the payment widget
        #                 const sumUpCard = window.SumUpCard;
        #                 console.log('SumUpCard is available.');
        #                 console.log('SumUpCard:', sumUpCard);                        
        #             } else {
        #                 console.error('SumUpCard is not available.');
        #             }
        #         }

        #         // Initialize SumUp Widget after the script is loaded
        #         document.addEventListener('DOMContentLoaded', function() {
        #             initSumUpWidget();
        #         });
        #     </script>
        # """, unsafe_allow_html=True)
        
        js_code = f"""
                    <div id="sumup-card"></div>
                    <script type="text/javascript" src="https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js"></script>
                    <script type="text/javascript">
                        SumUpCard.mount({{
                            id: 'sumup-card',
                            checkoutId: '{checkout_id}',
                            donateSubmitButton: false,
                            showInstallments: true,
                            onResponse: function (type, body) {{
                            console.log('Type', type);
                            console.log('Body', body);
                            }},
                        }});
                    </script>
                    """
        # st.write(js_code)
        with st.container():
            components.html(js_code, height=600)


@st.dialog("This is a dialogue")
def sumup_widget_component(checkout_id):
    st.markdown("<div id='sumup-card'></div>", unsafe_allow_html=True)

    js_code = f"""
        async function loadSumUpSDK() {{
            return new Promise((resolve, reject) => {{
                const script = document.createElement('script');
                script.src = "https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js";
                script.onload = () => resolve();
                script.onerror = () => reject(new Error('Failed to load SumUp SDK'));
                document.head.appendChild(script);
            }});
        }}
        async function initializeSumUpCard() {{
            await loadSumUpSDK();
            SumUpCard.mount({{
                id: 'sumup-card',
                checkoutId: '{checkout_id}',
                donateSubmitButton: false,
                showInstallments: true,
                onResponse: function (type, body) {{
                    console.log('Type', type);
                    console.log('Body', body);
                    SumUpCard.unmount();
                }},
            }});
        }}

        initializeSumUpCard();
        """
    response = stjs(js_code)
    if response:
        st.write(response)
        
def main():

    st.title("SumUp Payment Integration")

    # print authorisation status
    if st.session_state['sumup'] is not None:
        st.info("Authorisation successful!")
    else:
        st.warning("Authorisation required!")
    
    amount = st.number_input("Amount", min_value=1, value=10)
    
    if st.button("Pay Now"):
        payment = create_payment(amount)
        if payment:
            st.write("Payment created successfully!")
            st.json(payment)
        else:
            st.write("Payment creation failed.")

    st.divider()

    st.write("Click the link below to authorize the app:")
    if st.button("Authorize", key="authorize"):
        sumup = OAuth2Session(
            base_url=base_url,
            client_id=st.secrets["sumup"]["CLIENT_ID"],
            client_secret=st.secrets["sumup"]["CLIENT_SECRET"],
            redirect_uri=redirect_uri,
        )

        st.write(sumup)
        st.write(sumup.authorization_url())
        st.write(sumup.state)
        st.session_state['sumup'] = sumup

    st.write("Click the link below to get your account details:")
    if st.button("Get Account Details", key="account"):
        connect_me()

    st.write("Click the link below to get a SumUp token:")
    if st.button("Get Token", key="token"):
        _sumup = st.session_state['sumup']
        _sumup.get('https://api.sumup.com/v0.1/me')
        try:
            token = get_sumup_token(_sumup)
            st.write(_sumup)
            st.info(f"Our SumUp token is: {token}")
        except Exception as e:
            st.write(e)

    st.write("Click the link below to create a SumUp checkout:")
    
    reference = st.text_input('Checkout Reference', value=generate_checkout_reference(6))
    amount = st.number_input('Amount', value=1.01, step=0.01)
    currency = st.text_input('Currency', value='EUR')
    email = st.text_input('Pay To Email', value = 'social.from.scratch@proton.me')
    description = st.text_input('Description')

    if st.button("Create Checkout", key="checkout"):
        checkout = create_sumup_checkout(reference, amount, currency, email, description)
        if checkout:
            st.json(checkout)
            
    st.write("Checkouts:")
    st.json(st.session_state['checkouts'])
    
    st.write("Click the link below to retrieve checkout info:")
    
    for checkout in st.session_state['checkouts']:
        if st.button(f"Get Checkout Info {checkout}", key=f"checkout_info_{checkout}"):
            checkout_info = get_checkout_info(checkout)
            st.json(checkout_info)
    
    st.write("Click the link below to process checkout:")
    for checkout in st.session_state['checkouts']:
        if st.button(f"Process {checkout}", key=f"checkout_process_{checkout}"):
            process = process_checkout(checkout)
            st.json(process)
            
    st.title("SumUp Payment Integration")
    for checkout in st.session_state['checkouts']:
        if st.button(f"Pay Now {checkout}", key=f"pay-{checkout}"):
            sumup_widget(checkout)
            
    st.title("SumUp Payment Component")
    for checkout in st.session_state['checkouts']:
        if st.button(f"Pay Now {checkout}", key=f"component-{checkout}"):
            sumup_widget_component(checkout)
            
if __name__ == '__main__':
    main()