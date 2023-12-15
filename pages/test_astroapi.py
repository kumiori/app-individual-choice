import streamlit as st
import sys
sys.path.append('lib/')

from libastro import ApiClient
import json



def run():
    client = ApiClient(st.secrets["prokerala"]["CLIENT_ID"], 
                       st.secrets["prokerala"]["CLIENT_SECRET"])
    result = client.get('v2/astrology/kundli/advanced', {
        'ayanamsa': 1,
        'coordinates': '23.1765,75.7885',
        'datetime': '2020-10-19T12:31:14+00:00'
    })
    st.write(json.dumps(result, indent=4))

if __name__ == '__main__':
    # st.write()
    run()
