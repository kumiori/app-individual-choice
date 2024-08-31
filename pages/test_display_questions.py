import streamlit as st
if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Questions and Perspectives",
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

import json
# from streamlit_authenticator import Authenticate

# from pages.test_alignment import get_next_image
import yaml
from yaml import SafeLoader

from lib.io import QuestionnaireDatabase as IODatabase
from streamlit_elements import elements, mui, nivo
import plotly.express as px
import numpy as np


import pandas as pd
from streamlit_elements import dashboard, elements, html, mui, nivo


if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()
    
if 'serialised_data' not in st.session_state:
    st.session_state["serialised_data"] = {}
    

# ============================== AUTH ===========================
with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = AuthenticateWithKey(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
fields_connect = {'Form name':'Connect', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}
fields_forge = {'Form name':'Forge access key', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}

# ===============================================================

from pages._sumup_lib import get_sumup_transaction_history, get_transaction_details, display_transaction_details

def parse_json_data(input_data):
    # Initialize counters for each category
    yes_count = 0
    no_count = 0
    uncertain_count = 0

    # Iterate through each dictionary in the list
    for item in input_data:
        for key, value in item.items():
            numeric_value = float(value)
            if numeric_value == 0:
                yes_count += 1
            elif numeric_value == 1:
                no_count += 1
            elif 0 < numeric_value < 1:
                uncertain_count += 1

    # Create the final structured list
    DATA = [
        {
            "id": "yes",
            "label": "Yes",
            "value": yes_count
        },
        {
            "id": "uncertain",
            "label": "Uncertain",
            "value": uncertain_count
        },
        {
            "id": "no",
            "label": "No",
            "value": no_count
        }
    ]

    return DATA


db = IODatabase(conn, "discourse-data")

def _scatter_layout(fig):
    # fig.update_layout(xaxis_title="Column", yaxis_title="Row")
    fig.update_xaxes(showgrid=False, showticklabels=False, showline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, showline=False)
# Set square aspect ratio
    fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1
    ),
    yaxis=dict(
        scaleanchor="x",
        scaleratio=1
    )
)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

def custom_tooltip(d):
    return {
        "background": "#fff",
        "padding": "9px 12px",
        "border": "1px solid #ccc",
        "color": "black",
        "fontSize": "12px",
        "fontWeight": "bold",
        "content": f"{d['serie']['id']}: {d['point']['data']['xFormatted']} - {d['point']['data']['yFormatted']}",
    }
    
def extend_date_range(date_counts, days_before=3, days_after=5):
    # Convert string dates to datetime objects for manipulation
    date_keys = [datetime.strptime(date, "%Y-%m-%d") for date in date_counts.keys()]
    min_date = min(date_keys)
    max_date = max(date_keys)

    # Create a new dictionary to store the extended dates
    extended_dates = {}

    # Add the days before the minimum date
    for x in range(1, days_before + 1):
        new_date = min_date - timedelta(days=x)
        extended_dates[new_date] = 0

    # Add the original date counts
    for date, count in date_counts.items():
        extended_dates[datetime.strptime(date, "%Y-%m-%d")] = count

    # Add the days after the maximum date
    for x in range(1, days_after + 1):
        new_date = max_date + timedelta(days=x)
        extended_dates[new_date] = 0

    # Convert the extended dates back to strings for the nivo bump chart
    extended_date_counts = {date.strftime("%Y-%m-%d"): count for date, count in extended_dates.items()}

    # Sort the dictionary by date
    extended_date_counts = dict(sorted(extended_date_counts.items()))

    return extended_date_counts


def fetch_and_display_personal_data(conn, kwargs):
    # Fetch all data from the "questionnaire" table
    table_name = kwargs.get('database')
    signature = kwargs.get('key')
    
    if 'path' in kwargs:
        path = kwargs.get('path')
        st.toast(f"Fetching {path} data from the {table_name} table.")
        response = conn.table(table_name).select(path).eq('signature', signature).execute()
        updated_at = conn.table(table_name).select("updated_at").eq('signature', signature).execute()
    else:
        st.toast(f"Fetching all data from the {table_name} table.")
        response = conn.table(table_name).select("*").eq('signature', signature).execute()

    # Check if there is any data in the response
    if response and response.data:
        data = response.data
        _data = []
        # Display the dataset
        # for item in data:
            # st.write(f"ID: {item['id']}")
            # updated_at = datetime.fromisoformat(item['updated_at'][:-6])
            # st.write(f"Preferences updated at: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            # st.write(f"Updated At: {item['updated_at']}")
            # st.write(data)
            # st.write(f"Signature: {item['signature']}")

            # # Parse and display personal data
            # personal_data = json.loads(item['personal_data'])
            # st.write("Personal Data:")
            # for key, value in personal_data.items():
            #     if key == "athena-range-dates":
            #         continue  # Skip displaying this key-value pair
            #     if isinstance(value, dict):
            #         st.write(f"- {key}: {value['value']}")
            #     else:
            #         st.write(f"- {key}: {value}")

            # # Convert and display datetime objects
            # if 'athena-range-dates' in personal_data:
            #     st.write("Athena stay - range dates:")
            #     for date_obj in personal_data['athena-range-dates']:
            #         date = datetime.datetime(date_obj['year'], date_obj['month'], date_obj['day'])
            #         st.write(date.strftime("%Y-%m-%d"))

            # # st.write("Path 001:", item['path_001'])
            # st.write("Created At:", item['created_at'])
    else:
        st.write(f"No data found in the {table_name} table.")
    return data

signature = st.session_state["username"]

intro_text = """
"""

if st.session_state['authentication_status'] is None:
    st.markdown("### Towards our conference in Athens _Europe in Discourse_")
    
    cols = st.columns([1,3,1])
    with cols[1]:
        st.markdown(intro_text)

if st.session_state['authentication_status']:
    st.toast('Initialised authentication model')
    authenticator.logout()
    st.write(f'`Your signature is {st.session_state["username"][0:4]}***{st.session_state["username"][-4:]}`')

    dataset = fetch_and_display_personal_data(conn, 
                                    {'database': 'discourse-data',
                                        'key': signature,
                                        'index': 'signature',
                                        'path': "practical_questions_01"})
    # st.write(dataset)
    
    # Parse the JSON object within the dataset
    practical_questions = json.loads(dataset[0]["practical_questions_01"])

    from datetime import date
    # Extract values
    departure = practical_questions["departure_location"]["value"]
    travel_modes = ', '.join(practical_questions["Travel modes:"]["value"])
    date_from = date(practical_questions["athena-range-dates"][0]["year"], practical_questions["athena-range-dates"][0]["month"], practical_questions["athena-range-dates"][0]["day"]).strftime("%B %d, %Y")
    date_to = date(practical_questions["athena-range-dates"][1]["year"], practical_questions["athena-range-dates"][1]["month"], practical_questions["athena-range-dates"][1]["day"]).strftime("%B %d, %Y")
    resonance = float(practical_questions["executive"]["value"])
    financial_support = practical_questions["Financial support"]["value"]
    financial_details = ', '.join(practical_questions["Financial details"]["value"])
    accommodation_feedback = practical_questions["accommodation_feedback"]["value"]
    liking = ["despise", "dislike", "am neutral with respect to", "like", "love"]
    # Map resonance value to corresponding text
    if resonance == 0:
        resonance_text = "yes, it's a good idea"
    elif resonance == 1:
        resonance_text = "no, it's not a good idea"
    elif 0 < resonance <= 0.5:
        resonance_text = "kinda good"
    else:
        resonance_text = "could be better"

    go_forward = practical_questions["go_forward"]["value"] == "Yes"

    # Generate the discursive text
    discursive_text = (
        f"Hello _Fellows_, I am planning to join the Athens conference departing from `{departure}` and using `{str.lower(travel_modes)}`, staying in Athens from `{date_from}` to `{date_to}`. During my stay, `I {'' if financial_support == 'Yes' else 'do not'} wish` for financial support, which includes `{financial_details}`. I `{liking[accommodation_feedback]}` the proposed accommodations (with a rating of `{accommodation_feedback} out of 5`). Finally, `{resonance_text}` to connect to the plenary session. I `am {'' if go_forward else 'not '}happy` to go forward."
    )

    st.write(discursive_text)    
    st.write(f'`My signature is {st.session_state["username"][0:4]}***{st.session_state["username"][-4:]}`')
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    if col1.button("Fetch all data"):
        response = conn.table('discourse-data').select('signature', 'updated_at', 'personal_data', 'practical_questions_01').execute()

        athena_dates = []
        alignment_values = []
        
        if response and response.data:
            data = response.data
            for entry in data:
                for key in ['personal_data', 'practical_questions_01']:
                    if entry[key]:
                        parsed_data = json.loads(entry[key])
                        if "athena-range-dates" in parsed_data:
                            athena_dates.append(
                                {'signature': entry['signature'], 'dates': parsed_data["athena-range-dates"]})
            
                # Step 1: Extract alingment values       
                if entry['practical_questions_01']:            
                    entry_align = json.loads(entry['practical_questions_01'])["executive"]["value"]
                    alignment_values.append({entry['signature']: entry_align})
                
            st.json(data, expanded=False)
            # st.json(alignment_values, expanded=True)
            date_ranges = []
            
            for entry in athena_dates:
                start_date = date(entry['dates'][0]['year'], entry['dates'][0]['month'], entry['dates'][0]['day'])
                end_date = date(entry['dates'][1]['year'], entry['dates'][1]['month'], entry['dates'][1]['day'])
                date_ranges.append((start_date, end_date, entry['signature']))

            date_counts = defaultdict(int)
            for entry in athena_dates:
                start_date = date(entry['dates'][0]['year'], entry['dates'][0]['month'], entry['dates'][0]['day'])
                end_date = date(entry['dates'][1]['year'], entry['dates'][1]['month'], entry['dates'][1]['day'])

                current_date = start_date
                while current_date <= end_date:
                    date_counts[current_date.isoformat()] += 1
                    current_date = current_date.fromordinal(current_date.toordinal() + 1)

            # Step 2: Calculate cumulative presence
            cumulative_counts = []
            sorted_dates = sorted(date_counts.keys())
            # print(sorted_dates)
            # st.write("sorted dates")
            # st.write(sorted_dates)
            # st.write("date counts")
            # st.write(date_counts)
            sorted_date_counts = dict(sorted(date_counts.items()))
            # st.write('sorted_date_counts')
            # st.write(sorted_date_counts)
            max_y = 17
            cumulative_sum = 0
            extended_counts = extend_date_range(date_counts, days_before=3, days_after=5)
            
            for d in extended_counts:
                # cumulative_sum += date_counts[d]
                cumulative_counts.append({"x": d, "y": max_y - extended_counts[d]})

            # Step 3: Format for Nivo Bump Chart

            nivo_bump_data = [{"id": "presence", "data": cumulative_counts}]
            # st.write(nivo_bump_data)
            
            with elements("nivo_charts"):
                    # Third element of the dashboard, the Media player.
                st.markdown("### Presence forecast in Athens")
                with mui.Box(sx={"height": 300}):
                        nivo.Bump(
                            data=nivo_bump_data,
                            colors={ "scheme": "nivo" },
                            lineWidth=7,
                            width=700,
                            height=300,
                            activeLineWidth=6,
                            inactiveLineWidth=3,
                            inactiveOpacity=0.15,
                            pointSize=10,
                            activePointSize=16,
                            inactivePointSize=0,
                            pointColor={ "theme": "background" },
                            pointBorderWidth=3,
                            activePointBorderWidth=3,
                            pointBorderColor={ "from": "serie.color" },
                            axisTop=None,
                            enableGridX=False,
                            enableGridY=False,
                            axisBottom={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "Days in Athens",
                                "legendPosition": "middle",
                                "legendOffset": 32,
                                "tickValues": ["2024-09-24", "2024-09-26", "2024-09-28", "2024-10-01"],

                            },
                            axisLeft={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "missing",
                                "legendPosition": "middle",
                                "legendOffset": -40
                            },
                            margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                            axisRight=None,
                            # tooltip=custom_tooltip,
                        )

            st.markdown("### Visualising aligning values")
            st.json(alignment_values, expanded=False)
            
            st.json(parse_json_data(alignment_values), expanded=False)
            
            DATA = parse_json_data(alignment_values)
    #         DATA = [
    #     {
    #         "id": "yes",
    #         "label": "Yes",
    #         "value": 3
    #     },
    #     {
    #         "id": "uncertain",
    #         "label": "Uncertain",
    #         "value": 3
    #     },
    #     {
    #         "id": "no",
    #         "label": "No",
    #         "value": 2
    #     }
    # ]       
            st.write(DATA)
            with elements("nivo_charts_alignment"):

                with mui.Box(sx={"height": 300}):
                    nivo.Waffle(
                        data=DATA,
                        total=20,
                        rows=5,
                        columns=4,
                        borderRadius={3},
                        # borderWidth=3,
                        emptyOpacity=0.15,
                        padding=3,
                        color_scheme="nivo",
                        legends=[
                            {
                                "anchor": "bottom",
                                "direction": "row",
                                "justify": False,
                                "translateX": 0,
                                "translateY": 56,
                                "itemsSpacing": 0,
                                "itemWidth": 100,
                                "itemHeight": 18,
                                "itemDirection": "left-to-right",
                                "itemOpacity": 0.85,
                                "itemTextColor": "#777",
                                "symbolSize": 12,
                            }
                        ]
                    )

            
            st.write(f"{len(alignment_values)} did express their alignment value.")
            """
            This is a good sign.
            """
            matrix_size = int(np.ceil(np.sqrt(len(data))))
            # st.write(f"Matrix size: {matrix_size}")
            matrix = np.full((matrix_size, matrix_size), .5)

            # Map the hash strings to indices
            hash_to_index = {list(d.keys())[0]: idx for idx, d in enumerate(alignment_values)}

            # Fill the matrix with the values from the dataset
            index = 0
            for i in range(matrix_size):
                for j in range(matrix_size):
                    if index < len(alignment_values):
                        hash_str, value = list(alignment_values[index].items())[0]
                        matrix[i, j] = float(value)  # Place the value in the matrix
                        index += 1
                        
            # matrix = np.random.rand(matrix_size, matrix_size)
            
            fig = px.scatter(x=np.arange(matrix_size).repeat(matrix_size),
                 y=np.tile(np.arange(matrix_size), matrix_size),
                 size=np.array([[100. for j in range(matrix_size)] for i in range(matrix_size) ]).flatten(),
                 color=matrix.flatten(),
                 size_max=50,
                 labels={"Row": "", "Column": ""},
                #  color_continuous_scale="Blues",
                #  color_continuous_scale="Blues",
                #  color_continuous_scale="Blues",
                 color_continuous_scale="PiYG",
                #  color_continuous_scale="Spectral",
                #  color_continuous_scale=[(0, "black"), (0.5, "gray"), (1, "white")],
                 range_color=[0, 1],
                 title="Matrix Visualization")
            _scatter_layout(fig)
            st.plotly_chart(fig)
            """
            ### Greys did not respond?
            """
    # Display a button to retrieve the transaction history
    if st.button('Retrieve Transaction History'):
        # Call the function to get the transaction history
        tx_history = get_sumup_transaction_history(10)
        # st.write(tx_history)
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
            num_transactions = st.number_input("Enter the number of transactions to dig:", min_value=1, max_value=100, value=10)

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


            filtered_transactions = []

            for transaction in transactions:
                # st.write(transaction.get("product_summary", ""))
                if "Social Contract from Scratch" in transaction.get("product_summary", ""):
                    filtered_transactions.append(transaction)
            
            transactions = filtered_transactions
            
            # Display the transaction details in a table
            if transactions:
                # transactions[0]
                st.write("Fetching Transaction Details")
                # st.table(transactions)
                # for transaction in transactions:
                #     display_transaction_details(transaction)

            else:
                st.write("No transactions to display.")
            # st.write(transactions)
            transaction_rows = []
            for transaction in transactions:
                row = {
                    "Amount": transaction["amount"],
                    "Timestamp": transaction["local_time"],
                    "Status": transaction["status"],
                    "Transaction Code": transaction["transaction_code"],
                    "Product": transaction.get("product_summary", "N/A"),
                    "Receipt_url": next((link["href"] for link in transaction.get("links", []) if link["rel"] == "receipt" and link["type"] == "image/png"), "N/A")
                }
                transaction_rows.append(row)

            # Convert to DataFrame for better display
            df = pd.DataFrame(transaction_rows)

            # Display the table in Streamlit
            # st.table(df)       
            st.write(df)
            
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

            # Filter the DataFrame for transactions with status 'SUCCESSFUL'
            df_successful = df[df['Status'] == 'SUCCESSFUL']
            df_failed = df[df['Status'] == 'FAILED']

            # Sum the amounts for all 'SUCCESSFUL' transactions
            total_amount = df_successful['Amount'].sum()
            st.write(f"Total transactions: {len(df)}")
            st.write(f"Total FAILED: {len(df_failed)}")
            st.write(f"Total Amount for SUCCESSFUL transactions: {total_amount}")

            # Create a time/amount chart
            fig = px.scatter(df_successful, x='Timestamp', y='Amount', color=px.Constant('SUCCESSFUL'), 
                            labels={'color': 'Status'}, title='Transaction Amounts Over Time')
            fig.add_scatter(x=df_failed['Timestamp'], y=df_failed['Amount'], mode='markers', 
                            name='FAILED', marker=dict(color='red', symbol='x'))

            # Customize the chart if needed
            fig.update_layout(xaxis_title='Time', yaxis_title='Amount')

            # Display the scatter plot in Streamlit
            st.plotly_chart(fig)

            # Compute the cumulative amount received
            df_successful = df_successful.sort_values(by='Timestamp')
            df_successful['Cumulative Amount'] = df_successful['Amount'].cumsum()

            # Create a cumulative graph of the amount received
            fig_cumulative = px.line(df_successful, x='Timestamp', y='Cumulative Amount', 
                                    title='Cumulative Amount Received Over Time')

            # Customize the cumulative chart if needed
            fig_cumulative.update_layout(xaxis_title='Time', yaxis_title='Cumulative Amount')

            # Display the cumulative plot in Streamlit
            st.plotly_chart(fig_cumulative)
            
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main', fields = fields_connect)
    st.warning('Please use your access key')
    
if __name__ == '__main__':
    pass