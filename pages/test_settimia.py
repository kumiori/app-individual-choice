import streamlit as st
import streamlit_survey as ss
import streamlit.components.v1 as components


# if st.secrets["runtime"]["STATUS"] == "Production":
#     st.set_page_config(
#         page_title="Positioning Portal",
#         page_icon="✨",
#         layout="wide",
#         initial_sidebar_state="collapsed"
#     )

#     st.markdown(
#         """
#     <style>
#         [data-testid="collapsedControl"] {
#             display: none
#         }
#     </style>
#     """,
#         unsafe_allow_html=True,
#     )


from lib.io import conn
from streamlit_extras.add_vertical_space import add_vertical_space 

from lib.texts import _stream_example, corrupt_string, _stream_once
from lib.geo import get_coordinates
from streamlit_extras.streaming_write import write as streamwrite 
import time
import json
import hashlib
from lib.io import fetch_and_display_data
st.write(st.secrets["runtime"]["STATUS"])
_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)

from lib.survey import CustomStreamlitSurvey
from lib.authentication import AuthenticateWithKeys
import streamlit_survey as ss
import yaml
from yaml.loader import SafeLoader

# Initialize read_texts set in session state if not present
if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

def check_existence(conn, signature):
    if signature == "":
        st.error("Please provide a signature.")
        return

    # Check if the signature already exists
    user_exists, count = conn.table("gathering") \
        .select("*") \
        .ilike('signature', f'%{signature}%') \
        .execute()

    return len(user_exists[1]) == 1

def insert_or_update_data(conn, data):
    try:
        # insert a new record
        user_exists = check_existence(conn, signature=data["signature"])
        # st.write(json.dumps(data))

        if user_exists:
            # update_query = conn.table("gathering").update(data).eq('signature', data["signature"]).execute()
            
            # if update_query:
            # else:
                # st.error("Failed to update data.")
            st.info("A signature already exists. Do you have your access key?")
            
            return False
        else:
            insert_result = conn.table('gathering').upsert(data).execute()
            st.info("You happily signed and luck does not exist, yet. Lucky you!")
            return True
            
    except Exception as e:
        st.error(f"Error inserting or updating data in the database: {str(e)}")

def qualitative_parametric(name, question, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    key=key,
    areas = areas,
    data_values  = [1, 2, 10],
    question = question)

with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)


if "access_key" not in st.session_state:
    print('access_key not in session state')
    st.session_state['access_key'] = ''
    print(st.session_state['access_key'])
    
authenticator = AuthenticateWithKeys(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
survey = CustomStreamlitSurvey()
            
def create_connection(key, kwargs = {}):
    authenticator = kwargs.get('authenticator')
    survey = kwargs.get('survey')
    # _location = survey.data['location']['value']
    _location = survey.data.get('location', {}).get('value', 'Venegono Superiore, Varese, Italy')
    st.write(_location)
    if st.session_state["authentication_status"] is None:
        try:
            if authenticator.register_user(' Check • Point ', location = _location,  preauthorization=False):
                st.success(f'Very good 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
                    💨 Here is one for your access ✨ <`{ authenticator.credentials["access_key"] }`> ✨.        \
                    Keep it in your pocket, add it to your wallet...keep it safe 💭. You will use it to re•open the connection 💫')
        except Exception as e:
            st.error(e)
            
    else:
        st.warning("We are already connected. Re•enter using your key, check the connection later.")


# 2 bedrooms sabatical house, rent income:
# interested in the other apt: 7-12d rental = 1500EUR+50

def main():
    # st.title("Welcome to the Singular Mapping. A solid proof? Forget, and Ask the moon: If If-Then is full, is still Luck a useful tool? \n ## We divide by zero. \n ## and it's just fuck*ng pitch black..")
    title = """
    ## This is the Settimia
    """

    """
        Dynamic information gathering platform
    # Artists/Collaborators/Investors
    
    Landing page with various options of explorations
    You're here because ....
    
    ## -\ we (the fellowship) ..self.
    ## We (we+you)
    ## ...
    ## ...
    ## Products (anything):
    # Q: where are you loc? 
    ## { globeViz }

    Importantly...
    { ourCoordinates } Astral Chart

    [for residence periods: dynamic group 3bd always
        - chef
        - painter/sculptor (inArt)
        - musician/dancer/writer (inXXX)]

    ## Collect applications (information)
        Your preferences, profiling.
        
    ## Receiving money
        "Paywall": QR codes (exec) or (diversion)
        Payment system test.
    ## (Internal Governance)
    
    
If collab:
...
If Apply:
...
If Invest:
	- financial product
	- business plan

11=EUR 

--------------------------

paywall

--------------------------

pdf
    """
    st.markdown(title)
    stream = st.empty()
    
    with stream:
        _stream, errors = corrupt_string(title, damage_parameter=0.0)
        st.title(f"System errors number {errors}")
        streamwrite(_stream_once(_stream, damage=0.5), unsafe_allow_html=True)
        # with st.spinner('...'):
            # time.sleep(3)
        streamwrite(_stream_once("## ...", damage=0.), unsafe_allow_html=True)

    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter

    col1, col2, col3 = st.columns(3)

    survey = ss.StreamlitSurvey("The Where?")


    access_keys = ["3074dac353f359537cbc2df98821c1ef",
                   "e447d257840306371622d4b9a8287969",
                   "7979ea222fa4d8052f2751ac6349f8f3",
                   "153bb8511021a4c8971614f098983bab",
                   "705a8a7237084f0d267f07690c614f73",
                   "e4917fdc9398c37d0f63cf5ac5666f78"]
    
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown("## Pick an access key >")
    
    with col2:
        for key in access_keys:
            st.markdown(f"`{key}`", unsafe_allow_html=True)
    st.divider()
   
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown("## ¿ What is your location")
    with col2:
        location = survey.text_input("location", help="Our location will appear shortly...", value=st.session_state.get('location', 'Venegono Superiore, Varese, Italy'))

    # create_connection("connection", kwargs = {"survey": survey, "authenticator": authenticator})
    authenticator.login('Do you already have a key?')
    
    st.divider()
    
    if st.session_state["authentication_status"]:
        st.success('Lovely! 🐉 Fellowship connected!')
        # st.session_state.current_discourse_page = 9
        
        authenticator.logout('Disconnect', 'main', key='disconnect')
    st.divider()
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    # with col2:
        # st.markdown("## ¿ What is your")
        # location = survey.text_input("_location", help="Our location will appear shortly...", value=st.session_state.location)
    
    if location is not None:
        coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
        st.session_state.coordinates = coordinates
        st.write(coordinates)
        with col1:
            st.markdown("## As a rule of thumb...")
            
        with col3:
            st.markdown("## Luck (y)")
            lucky_number = survey.number_input("number", min_value=0, max_value=1000000000)

        # Send Data Button
        if col1.button(f"Check in from {location}"):
            data = {
                "location": survey.data["location"]["value"],
                "latitude": coordinates[0],
                "longitude": coordinates[1],
                "coordinates": coordinates,
                "luckynumber": survey.data["number"]["value"]
            }

            signature = hashlib.md5(str(data).encode('utf-8')).hexdigest()
            # st.write("")
            data["signature"] = signature

            # Update session state with the signature
            st.session_state.signature = signature

            newdata = insert_or_update_data(conn, data)

            if newdata:
                st.success(f"This is your signature \n`` {signature} ``. Keep it in your files, it will allow swift access...")
            else:
                _default = data["location"]+"-"+str(data["luckynumber"])
                access = survey.text_input("signature", help="Your fingerprint.")
                
        
        col1, col3, col3 = st.columns(3) 
                       
        if hasattr(st.session_state, 'coordinates'):
            if col2.button("Update our Map"):
                data = fetch_and_display_data(conn, kwargs={"database":"gathering"})
                
                stream.markdown("# This is how the moon sees the planet revolving...")
                # with stream:
                    # st.write('.........')
                
                # Generate JavaScript code with city data
                javascript_code = f"""
                // Gen city data
                const VELOCITY = 9; // minutes per frame

                const sunPosAt = dt => {{
                    const day = new Date(+dt).setUTCHours(0, 0, 0, 0);
                    const t = solar.century(dt);
                    const longitude = (day - dt) / 864e5 * 360 - 180;
                    return [longitude - solar.equationOfTime(t) / 4, solar.declination(t)];
                }};

                let dt = +new Date();
                const solarTile = {{ pos: sunPosAt(dt) }};
                const timeEl = document.getElementById('time');

                const cityData = { data };
                const N = 10;

                const world = Globe()
                    (document.getElementById('globeViz'))
                    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
                    .backgroundColor('rgb(14, 17, 23)')
                    .tilesData([solarTile])
                    .tileLng(d => d.pos[0])
                    .tileLat(d => d.pos[1])
                    .tileAltitude(0.01)
                    .tileWidth(180)
                    .tileHeight(180)
                    .tileUseGlobeProjection(false)
                    .tileMaterial(() => new THREE.MeshLambertMaterial({{ color: '#ffff00', opacity: 0.3, transparent: true }}))
                    .tilesTransitionDuration(0)
                    .pointsData(cityData)
                    .pointAltitude('luckynumber');

                // animate time of day
                requestAnimationFrame(() =>
                    (function animate() {{
                    dt += VELOCITY * 60 * 1000;
                    solarTile.pos = sunPosAt(dt);
                    world.tilesData([solarTile]);
                    timeEl.textContent = new Date(dt).toLocaleString();
                    requestAnimationFrame(animate);
                    }})()
                );

                // Add auto-rotation
                world.controls().autoRotate = true;
                world.controls().autoRotateSpeed = 3.6;
                """

                # HTML code with embedded JavaScript
                html_code = f"""
                <head>
                <style> body {{ margin: 0em; }} </style>
                <script src="//unpkg.com/three"></script>
                <script src="//unpkg.com/globe.gl"></script>
                <script src="//unpkg.com/solar-calculator"></script>
                </head>

                <body>
                <div id="globeViz"></div>
                <div id="time"></div>
                <script>
                    { javascript_code }
                </script>
                </body>
                """

                # Display the HTML code in Streamlit app
                col1, col2 = st.columns(2)
                with col1:
                    st.components.v1.html(html_code, height=700, width=700)
                
                

# Run the app
if __name__ == "__main__":
    main()

