import streamlit as st
if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Financials",
        page_icon="👋",
        initial_sidebar_state="collapsed"
    )
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        [data-testid="stHeader"] {
            display: none
            }
    </style>
    """,
        unsafe_allow_html=True,
    )
from lib.io import (
    conn
)
# from lib.texts import stream_text, _stream_once
import lib.texts as texts
from datetime import datetime, timedelta
from philoui.authentication_v2 import AuthenticateWithKey
# from philoui.io import check_existence
from collections import defaultdict
import pandas as pd
import json
# from streamlit_authenticator import Authenticate
from sumup_oauthsession import OAuth2Session

# from pages.test_alignment import get_next_image
import yaml
from yaml import SafeLoader
import re

from lib.io import QuestionnaireDatabase as IODatabase
from streamlit_elements import elements, mui, nivo
import plotly.express as px
import numpy as np

from pages._sumup_lib import get_sumup_transaction_history, get_transaction_details, display_transaction_details

# Initialize the session state for 'show_successful_only'
if 'show_successful_only' not in st.session_state:
    st.session_state['show_successful_only'] = False
    
# Initialize session state for card ownership if not already present
if 'owned_cards' not in st.session_state:
    st.session_state['owned_cards'] = set()
    
def parse_payment_data(payment_data):
    aggregated = []
    print(len(payment_data))
    # Using structural pattern matching to extract relevant information
    for transaction in payment_data:
        result = {}
        match transaction:
            case {
                "amount": amount,
                "card": {"last_4_digits": last_4_digits, "type": card_type},
                "currency": currency,
                "location": {"lat": lat, "lon": lon},
                "status": status,
                # "payout_date": payout_date,
                "timestamp": timestamp,
                "product_summary": product_summary,
                "id": id,
                "events": events,
                "links": links,
                # "products": [{"name": product_name, "price": price}],
                # "username": username,
            }:
                # Collecting relevant information
                result["amount"] = amount
                result["currency"] = currency
                result["last_4_digits"] = last_4_digits
                result["card_type"] = card_type
                result["lat"] = lat
                result["lon"] = lon
                result["status"] = status
                # result["payout_date"] = payout_date
                result["timestamp"] = timestamp
                result["id"] = id
                
                            # Check if "Social Contract from Scratch" is in the product_summary
                if "Social Contract from Scratch" in product_summary:
                    result['product_summary'] = product_summary
                    contract_info = product_summary.split('•')
                    if len(contract_info) > 1:
                        result['contract_name'] = contract_info[0].strip()
                        result['contract_code'] = contract_info[1].strip()
                    else:
                        result['contract_name'] = "Unknown"
                        result['contract_code'] = "Unknown"
                else:
                    result['product_summary'] = product_summary


                # Handling events
                event_data = []
                for event in events:
                    match event:
                        case {"amount": event_amount, "status": event_status, "timestamp": event_timestamp, "payout_reference": payout_reference}:
                            event_data.append({
                                "amount": event_amount,
                                "status": event_status,
                                "timestamp": event_timestamp,
                                "payout_reference": payout_reference,
                            })
                result['events'] = event_data

                # Extracting receipt link (PNG format)
                receipt_link = None
                for link in links:
                    match link:
                        case {"href": href, "type": "image/png"}:
                            receipt_link = href
                result['receipt_link'] = receipt_link

                # result["product_name"] = product_name
                # result["price"] = price
                # result["username"] = username

            # Case 3: Minimal data
            case {
                "amount": amount,
                "currency": currency,
                "timestamp": timestamp,
                "product_summary": product,
                "status": status,
            }:
                result["amount"] = amount
                result["currency"] = currency
                result["timestamp"] = timestamp
                result["product_summary"] = product
                result["status"] = status

            case _:
                print("The provided data does not match the expected format.")
                result["amount"] = "nan"
                
        aggregated.append(result)

    return aggregated


def parse_payment_data2(payment_data):
    aggregated = []
    print(len(payment_data))
    # Using structural pattern matching to extract relevant information
    for transaction in payment_data:
        aggregated.append(process_transaction(transaction))
    return aggregated

def process_common_fields(transaction):
    """Handles fields that are common across all transactions."""
    result = {}
    match transaction:
        case {
            "amount": amount,
            "status": status,
            "payment_type": payment_type,
            "currency": currency,
            "timestamp": timestamp,
            "id": id,
        }:
            result['amount'] = amount
            result['status'] = status
            result['payment_type'] = payment_type
            result['currency'] = currency
            result['timestamp'] = timestamp
            result['id'] = id
    return result


def process_events(events):
    """Handles the processing of events inside a transaction."""
    event_data = []
    for event in events:
        match event:
            case {
                "amount": event_amount,
                "status": event_status,
                "timestamp": event_timestamp,
                "payout_reference": payout_reference
            }:
                event_data.append({
                    "amount": event_amount,
                    "status": event_status,
                    "timestamp": event_timestamp,
                    "payout_reference": payout_reference,
                })
    return event_data


def process_links(links):
    """Handles the links in the transaction to extract receipt links (PNG format)."""
    receipt_link = None
    for link in links:
        if link.get("type") == "image/png":
            receipt_link = link.get("href")
    return receipt_link


def process_product_summary(product_summary):
    """Processes the product summary, especially if it's a 'Social Contract from Scratch'."""
    result = {}
    if "Social Contract from Scratch" in product_summary:
        result['product_summary'] = product_summary
        contract_info = product_summary.split('•')
        if len(contract_info) > 1:
            result['contract_name'] = contract_info[0].strip()
            result['contract_code'] = contract_info[1].strip()
        else:
            result['contract_name'] = "Unknown"
            result['contract_code'] = "Unknown"
    else:
        result['product_summary'] = product_summary
    return result


def process_transaction(transaction):
    """Processes the entire transaction, handling common fields and specific transaction types."""
    result = {}

    # Process common fields
    result.update(process_common_fields(transaction))

    # Handle specific transaction details
    match transaction:
        case {
            "card": {"last_4_digits": last_4_digits, "type": card_type},
            "events": events,
            "links": links,
            "product_summary": product_summary,
            "location": {"lat": lat, "lon": lon},
        }:
            result['last_4_digits'] = last_4_digits
            result['card_type'] = card_type
            result['events'] = process_events(events)
            result['receipt_link'] = process_links(links)
            result["lat"] = lat
            result["lon"] = lon
            result.update(process_product_summary(product_summary))

        case {
            # "events": events,
            "links": links,
            "product_summary": product_summary,
        }:
            # Handle non-card transactions, e.g., API payments
            # result['events'] = process_events(events)
            result['receipt_link'] = process_links(links)
            result.update(process_product_summary(product_summary))

        case _:
            print(transaction)
            print("Transaction does not match the expected format.")

    return result



@st.cache_data(ttl=600)
def get_sumup_history(num_transactions):
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

        # st.table(transaction_rows)
        # st.write(transaction_rows)
    
        # Retrieve and display transactions
        transactions = []
        my_bar = st.progress(0, "Fetching transaction details")

        for i in range(num_transactions):
            my_bar.progress((i+1)/num_transactions)
            # For demonstration, we'll use the loop index as the transaction ID
            transaction_id = transaction_rows[i]["Transaction ID"]
            # st.write(f"Fetching transaction details for ID: {transaction_id}")
            transaction_details = get_transaction_details(transaction_id)
            transactions.append(transaction_details)

        # filtered_transactions = []

        # for transaction in transactions:
        #     st.write(transaction.get("product_summary", ""))
        #     if "Social Contract from Scratch" in transaction.get("product_summary", ""):
        #         filtered_transactions.append(transaction)
        # return 

        # transactions = filtered_transactions

        # Display the transaction details in a table
        if transactions:
            # transactions[0]
            st.write("### Transactions Details")
            # st.json(transactions[0])
            # st.table(transactions)
            # for transaction in transactions:
            #     display_transaction_details(transaction)

        else:
            st.write("No transactions to display.")
        # st.write(transactions)
        
        return transactions
    

if __name__ == '__main__':
    # st.write(st.secrets["sumup"])
    
    redirect_uri = "https://social-contract-from-scratch.streamlit.app/"
    base_url = "https://api.sumup.com/"

    sumup = OAuth2Session(
        base_url=base_url,
        client_id=st.secrets["sumup"]["CLIENT_ID"],
        client_secret=st.secrets["sumup"]["CLIENT_SECRET"],
        redirect_uri=redirect_uri,
    )

    if DEBUG:=False:
        st.write(sumup)
        st.write(sumup.authorization_url())
        st.write(sumup.state)   


    num_transactions = st.number_input("Enter the number of transactions to dig:", min_value=1, max_value=100, value=10)
    transactions = get_sumup_history(num_transactions)
    
    result = parse_payment_data2(transactions)
    # st.write(result)
    # Toggle to show only successful transactions
    df = pd.DataFrame(result)

    st.session_state['show_successful_only'] = st.checkbox("Show only successful transactions", value=st.session_state['show_successful_only'])

    # Filter the DataFrame based on the toggle
    if st.session_state['show_successful_only']:
        print("Filtering successful transactions")
        df = df[df["status"] == "SUCCESSFUL"]

    id = st.number_input("Enter the # of transaction to dig:", min_value=0, max_value=num_transactions-1, value=1)
    st.json(transactions[id], expanded=False)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # # Filter the DataFrame for transactions with status 'SUCCESSFUL'
    df_successful = df[df['status'] == 'SUCCESSFUL']
    df_failed = df[df['status'] == 'FAILED']

    # # Sum the amounts for all 'SUCCESSFUL' transactions
    total_amount = df_successful['amount'].sum()
    st.write(f"Total transactions: {len(df)}")
    st.write(f"Total FAILED: {len(df_failed)}")
    st.write(f"Total Amount for SUCCESSFUL transactions: {total_amount}")

    # Create a time/amount chart
    fig = px.scatter(df_successful, x='timestamp', y='amount', color=px.Constant('SUCCESSFUL'), 
                    labels={'color': 'Status'}, title='Transaction Amounts Over Time')
    fig.add_scatter(x=df_failed['timestamp'], y=df_failed['amount'], mode='markers', 
                    name='FAILED', marker=dict(color='red', symbol='x'))

    # Customize the chart if needed
    fig.update_layout(xaxis_title='Time', yaxis_title='Amount')

    # Display the scatter plot in Streamlit
    st.plotly_chart(fig)

    # Compute the cumulative amount received
    df_successful = df_successful.sort_values(by='timestamp')
    df_successful['Cumulative Amount'] = df_successful['amount'].cumsum()

    # Create a cumulative graph of the amount received
    fig_cumulative = px.line(df_successful, x='timestamp', y='Cumulative Amount', 
                            title='Cumulative Amount Received Over Time')

    # Customize the cumulative chart if needed
    fig_cumulative.update_layout(xaxis_title='Time', yaxis_title='Cumulative Amount')

    # Display the cumulative plot in Streamlit
    st.plotly_chart(fig_cumulative)

    "### CC: Display the last 4 digits of the card used in the transactions"
    card_last_digits = set(df["last_4_digits"])
    st.write(card_last_digits)

    st.write("Select the last 4 digits of your card:")

    # Display checkboxes for each card
    for card in card_last_digits:
        is_checked = st.checkbox(f"Card ending in {card}", value=(card in st.session_state['owned_cards']))
        
        # Add or remove cards based on user selection
        if is_checked:
            st.session_state['owned_cards'].add(str(card))
        else:
            st.session_state['owned_cards'].discard(str(card))
    
    
    # Display owned cards
    if st.session_state['owned_cards']:
        st.write("You have declared ownership of the following cards:")
        # st.write(", ".join(st.session_state['owned_cards']))
        st.write(st.session_state['owned_cards'])
    else:
        st.write("No card ownership declared yet.")
        
    "### Named transactions " 
    # st.table(df["contract_code"])
    # st.table(df[df['contract_code'].notnull()])
           
    # Function to extract names from the contract_code
    def extract_name(contract_code):
        pattern = r"SCFS11111-S-([A-Za-z\-]+)-\d+"
        match = re.search(pattern, str(contract_code))
        if match:
            return match.group(1)
        return None

    df_non_null = df[df['contract_code'].notnull()]

    df_non_null['payer_name'] = df_non_null['contract_code'].apply(extract_name)
    
    df['payer_name'] = df['contract_code'].apply(extract_name)
    df_with_names = df[df['payer_name'].notnull()]
    st.table(df_with_names[["id", "amount", "timestamp", "payer_name"]])
    # Display the dataframe with extracted names

    "## Card payments"
    file_path = 'data/MCTFDRN220241019.csv'
    card_transactions = pd.read_csv(file_path)

    # Convert the dataframe to a Python dictionary
    card_transaction_dict = df.to_dict(orient='records')

    st.table(card_transactions[card_transactions["Type de transaction"] != "Paiement entrant SumUp"])
    
    card_transactions = card_transactions[card_transactions["Type de transaction"] != "Paiement entrant SumUp"]
    
    # card_df = pd.DataFrame(card_payments)

    card_transactions["personal_expense"] = False

    # Let the user mark transactions as personal expenses
    for idx, row in card_transactions.iterrows():
        card_transactions.at[idx, "personal_expense"] = st.checkbox(f"Mark as personal: {row['Référence'], row['Montant facturé débité']}", value=False, key=f"checkbox_{idx}")

    # Filter to show only collective expenses
    collective_df = card_transactions[card_transactions["personal_expense"] == False]

    # Display the filtered DataFrame
    st.json(collective_df.to_json(orient='records'))
    
    # Compute the cumulative amount received
    collective_df['timestamp'] = pd.to_datetime(collective_df['Date de la transaction'])
    collective_df = collective_df.sort_values(by='timestamp', ascending=True)
    collective_df['Cumulative Amount'] = collective_df["Montant facturé débité"].cumsum()
    
    # # Create a cumulative graph of the amount received
    # fig_cumulative = px.line(collective_df, x='timestamp', y='Cumulative Amount', 
    #                         title='Cumulative Expenses Over Time')

    # fig_cumulative = px.line(df_successful, x='timestamp', y='Cumulative Amount', 
    #                         title='Cumulative Amount Received Over Time')

    # # Customize the cumulative chart if needed
    # fig_cumulative.update_layout(xaxis_title='Time', yaxis_title='Cumulative Amount')

    # # Display the cumulative plot in Streamlit
    # st.plotly_chart(fig_cumulative)
    # Create a figure using Plotly's graph_objects

    # Merge the two dataframes on 'timestamp', with an outer join to retain all timestamps
    # Check and localize timestamps if necessary, then convert to UTC
    if df_successful['timestamp'].dtype == 'datetime64[ns]':  # Naive timestamps
        df_successful['timestamp'] = df_successful['timestamp'].dt.tz_localize('UTC')
    else:
        df_successful['timestamp'] = df_successful['timestamp'].dt.tz_convert('UTC')

    if collective_df['timestamp'].dtype == 'datetime64[ns]':  # Naive timestamps
        collective_df['timestamp'] = collective_df['timestamp'].dt.tz_localize('UTC')
    else:
        collective_df['timestamp'] = collective_df['timestamp'].dt.tz_convert('UTC')

    financials_df = pd.merge(df_successful[['timestamp', 'Cumulative Amount']], 
                        collective_df[['timestamp', 'Cumulative Amount']], 
                        on='timestamp', 
                        how='outer', 
                        suffixes=('_incoming', '_expenses'))

    # Fill NaN values with 0 for easier subtraction (or handle them differently if needed)
    financials_df = financials_df.fillna(0)

    # Calculate the difference between the cumulative amounts
    financials_df['Difference'] = financials_df['Cumulative Amount_incoming'] - financials_df['Cumulative Amount_expenses']

    import plotly.graph_objects as go

    fig_cumulative = go.Figure()

    # Add the first line for 'collective_df'
    fig_cumulative.add_trace(go.Scatter(x=collective_df['timestamp'], y=-collective_df['Cumulative Amount'],
                                        mode='lines', name='Cumulative Expenses'))

    # Add the second line for 'df_successful'
    fig_cumulative.add_trace(go.Scatter(x=df_successful['timestamp'], y=df_successful['Cumulative Amount'],
                                        mode='lines', name='Cumulative Amount Received'))

    # fig_cumulative.add_trace(go.Scatter(x=financials_df['timestamp'], y=financials_df['Difference'],))
    
    # Customize the cumulative chart
    fig_cumulative.update_layout(title='Cumulative Expenses and Amount Received Over Time',
                                xaxis_title='Time', yaxis_title='Cumulative Amount')

    # Display the cumulative plot in Streamlit
    st.plotly_chart(fig_cumulative)