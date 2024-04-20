import streamlit as st
from sumup_oauthsession import OAuth2Session
import requests
import json

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
    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json().get('access_token')
        st.success(f'Success! Access token: {access_token}')
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')


def main():

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
    # sumup.authorize()

    # Define the SumUp API endpoint URL
    api_url = 'https://api.sumup.com/v0.1/me'

    # Define the authorization header with your SumUp API token
    headers = {
        'Authorization': 'Bearer sup_sk_H9jiW4mVDTquAr4eUQ8aJ2uleh8mYDcYj'
    }

    # Make an HTTP GET request to the SumUp API endpoint
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Display the response data
        st.success(f'Response: {response.json()}')
        pretty_json = json.dumps(response.json(), indent=4)
        st.json(pretty_json)
    else:
        # Display an error message if the request failed
        st.error(f'Error: {response.text}')

    if st.button('Generate SumUp Token'):
        get_sumup_token()



if __name__ == '__main__':
    main()