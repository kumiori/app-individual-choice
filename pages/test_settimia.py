import hashlib
import json
import random
import time

import streamlit as st
import streamlit.components.v1 as components
import streamlit_survey as ss
from lib.geo import get_coordinates
from lib.io import conn, create_equaliser, fetch_and_display_data, QuestionnaireDatabase
from lib.texts import _stream_example, _stream_once, corrupt_string
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row
from streamlit_extras.streaming_write import write as streamwrite



st.write(st.secrets["runtime"]["STATUS"])
_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)

import streamlit_survey as ss
import yaml
from lib.authentication import AuthenticateWithKeys, GateAuthenticate
from lib.survey import CustomStreamlitSurvey
from yaml.loader import SafeLoader

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


# Initialize read_texts set in session state if not present
if 'read_texts' not in st.session_state:
    st.session_state["read_texts"] = set()

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
            st.info("You signed and luck does not exist, yet. Lucky you!")
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

with open('data/credentials_settimia.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

if "access_key" not in st.session_state:
    st.session_state['access_key'] = ''

if 'selected_idea' not in st.session_state:
    st.session_state["selected_idea"] = None

if 'selected_name' not in st.session_state:
    st.session_state["selected_name"] = None
    
def clear_session_state():
    st.session_state["selected_name"] = None
    st.session_state["selected_idea"] = None


# authenticator = AuthenticateWithKeys(
authenticator = GateAuthenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['cookie']['expiry_minutes'],
    config['preauthorized'],
    webapp='settimia'
)

survey = CustomStreamlitSurvey()
            
def create_connection(key, kwargs = {}):
    authenticator = kwargs.get('authenticator')
    survey = kwargs.get('survey')
    data = kwargs.get('data')
    # st.write(data)
    # _location = survey.data.get('location').get('value', 'Venegono Superiore, Varese, Italy')
    if st.session_state["authentication_status"] is None:
        try:
            if authenticator.register_user(' Check • Point ', data = data, match = True, preauthorization=False):
                st.success(f'Very good 🎊. We have created ourselves a new key 🗝️.\
                    💨 This means ✨ <`{ authenticator.credentials["access_key"] }`>.        \
                    Keep it safe 💭. You will use it to re•open the connection 💫')
        except Exception as e:
            st.error(e)
            
    else:
        st.warning("We are already connected. Re•enter using your key, check the connection later.")
        # authenticator.logout('Disconnect', 'main', key='disconnect')


def account_for_data(db, username, data):
    try:
        # data_json = json.loads(data)
        db.insert_or_update_data(username, data)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")

    
def main():
    # st.title("Welcome to the Singular Mapping. A solid proof? Forget, and Ask the moon: If If-Then is full, is still Luck a useful tool? \n ## We divide by zero. \n ## and it's just fuck*ng pitch black..")
    title = """
    # This is Settimia
    """

    st.markdown(title)
    stream = st.empty()
    
    with stream:
        _stream, errors = corrupt_string(title, damage_parameter=0.0)
        st.markdown(f"`System errors number {errors}`")
        streamwrite(_stream_once(_stream, damage=0.5), unsafe_allow_html=True)
        # with st.spinner('...'):
            # time.sleep(3)
        streamwrite(_stream_once("## ...", damage=0.), unsafe_allow_html=True)

    if 'location' not in st.session_state:
        st.session_state["location"] = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state["coordinates"] = None  # Initial damage parameter

    col1, col2, col3 = st.columns(3)

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
   
   
    st.markdown("## Let's get started creating a new key")
   
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        if st.button("Clear Memory"):
            clear_session_state()
            st.info("Session state cleared.")
    
    def commit_to_state(data_type, value):
        if data_type == "name":
            st.session_state["selected_name"] = value
        elif data_type == "idea":
            st.session_state["selected_idea"] = value


    if st.session_state["selected_name"] is None:
        st.title("Match the Name with the ✨!")
    else:
        st.title(f"Match *{st.session_state['selected_name']}* with the 'moji!")
   
    names = ["Andrew", "Leslie", "Mai-Brit", "Giampaolo", "Andrés", "Victoria", "Settimia"]
    ideas = list(set(["🦇", "✨", "👽", "😗", "🥹", "♥️", "❤️‍🔥", "🫠", "🥴", "👀", "🧞‍♂️", "🐎", "💫", "💨", "🏢", "🇫🇷", "☑️", "🔑", "🥖", "🕘", "🚧", "🪽", "✨", "☀️", "🔥", "🫂", "🧜🏾‍♂️", "👋🏾", "✉️", "🥤", "🚪", "💃", "🫡", "🎭", "🧉", "⏰", "🦹", "🕛", "🕶️", "💥", "🔐", "🕯️", "❤️", "🤌", "🇮🇹", "🍝", "🍕", "♾️", "🙏", "👏", "🔥", "🍷", "🪵", "☀️", "💞", "🌽", "💦", "💥", "🌻", "🎉", "🪄", "😎", "🗝️", "🛎️", "🧡", "🗝", "🚪", "🧼", "🧿", "💳", "💋", "🥩", "🧂", "🐚", "💦"]))
    random.shuffle(names)
    random.shuffle(ideas)


    def check_answer():
        return True
    
        
    def display_ideas(icon_row, _ideas):
        for word in _ideas:
            if icon_row.button(
                    word,
                    key = f"button_{word}",
                    use_container_width=True,
                    on_click = commit_to_state, args = ["idea", word]):
                st.session_state["selected_idea"] = word
                if st.session_state["selected_name"] is not None:
                    check_answer()

    if st.session_state["selected_name"] is None:
        icon_row = row(3)
        for num in names:
            if icon_row.button(
                str(num),
                key = f"button_{num}",
                use_container_width=True,
                on_click = commit_to_state, args = ["name", num]):
                st.session_state["selected_name"] = num
                if st.session_state["selected_idea"] is not None:
                    check_answer()
    else:
        col1.markdown(
            f"# {st.session_state['selected_name']}",
            unsafe_allow_html=True,
        )
    col1, col2, col3 = st.columns([1, 1.2, 1])

    if st.session_state["selected_idea"] is None:
        icon_row = row(6)
        _ideas = ideas[0:19]+["..."]
        display_ideas(icon_row, _ideas)
        
    elif st.session_state["selected_idea"] == "...":
        icon_row = row(6)
        _ideas = ideas[19::]+["∣"]
        display_ideas(icon_row, _ideas)
        
    else:
        col3.markdown(
            f"# {st.session_state['selected_idea']}",
            unsafe_allow_html=True,
        )
    st.write('''<style>
        [data-testid="stVerticalBlock"] [data-testid="baseButton-secondary"] p {
            font-size: 2rem;
            padding: 1rem;
        }
    </style>''', unsafe_allow_html=True)
    
    match = True
    if st.session_state["selected_name"] is not None and st.session_state["selected_idea"] is not None:
        # col1, col2, col3 = st.columns([1, 1.2, 1])
        col1.markdown(
            f"# {st.session_state['selected_name']}",
            unsafe_allow_html=True,
        )
        # col3.markdown(
        #     f"# {st.session_state['selected_idea']}",
        #     unsafe_allow_html=True,
        # )
        if col2.button("Check Answer"):
            st.success("Yes", icon="✨")
            # match = check_answer()
            # st.info(correct_association[st.session_state["selected_idea"]]["question"])
        # st.json(st.session_state, expanded=False)
    
        create_connection(key = "authors", kwargs = {"survey": survey, 
                                                     "authenticator": authenticator,
                                                     "data": {"name": st.session_state["selected_name"],
                                                              "idea": st.session_state["selected_idea"]}, 
                                                     "match": check_answer()})


   
    # create_connection("connection", kwargs = {"survey": survey, "authenticator": authenticator})
    authenticator.login('Do you already have a key?')
    col1, col2, col3 = st.columns([1, 1.2, 1])
        
    with col1:
        if st.button('Show Key'):
            # st.write(st.session_state)
            col2.markdown(f"{st.session_state['access_key']}")
    with col3:
        authenticator.logout('Disconnect', 'main', key='disconnect2')

    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col1:
        st.markdown("## ¿ What is your location")
    with col2:
        location = survey.text_input("location", help="Our location will appear shortly...", value=st.session_state.get('location', 'Venegono Superiore, Varese, Italy'))

    st.divider()
    st.write(f'Auth {st.session_state["authentication_status"]}')
    
    if st.session_state["authentication_status"]:
        st.success('Lovely! 🐉 Fellowship connected! Here\'s a story to be told 👇')
        # st.session_state.current_discourse_page = 9
        
        """🦇✨👽😗🥹♥️❤‍🔥🫠🥴👀🧞‍♂️🐎
        💫💨🏢🇫🇷☑️🔑🥖🕘🚧🪽✨☀️🔥🫂🧜🏾‍♂️👋🏾✉️🥤🚪💃🫡🎭🧉⏰🦹🕛🕶️💥🔐🕯️
        ❤️🤌🇮🇹🍝🍕♾️🙏👏🔥🍷🪵☀️💞🌽💦💥🌻🎉🪄😎🗝️🛎️
        🧡🗝🚪🧼🧿💳💋🥩🧂🐚💦
        """        
        # authenticator.logout('Disconnect', 'main', key='disconnect')
        st.divider()
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        if location is not None:
            coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
            st.session_state.coordinates = coordinates
            st.write(coordinates)
                
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
                # data["signature"] = signature

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
        
        equaliser_data = [
            ("Social Media Presence", ""),
            ("Conceptual/Business", ""),
            ("Investor Relations", ""),
            ("Product Development", ""),
            ("Event Planning", ""),
        ]

        # st.write(survey)
        st.markdown("## Let's think _energetically..._")
        st.markdown("### Using an _energy_ mixer, where _should_ energy go?")
        create_equaliser(key = "equaliser", kwargs={"survey": survey, "data": equaliser_data})

        data = survey.data

        db = QuestionnaireDatabase(conn, "settimia")
        
        # st.json(data)
        if st.button(f"Account for preferences, signature: {st.session_state['access_key']}"):
            try:
                locator = {'key': st.session_state['access_key'], 'label': 'signature'}
                account_for_data(db, locator, data = {'label': 'data', 'record': data})
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please provide a valid JSON string.")


        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        if col1.button("Fetch Data"):
            _data = db.fetch_data()
            
        col3.download_button(
            label="Download raw",
            data=survey.to_json(),
            file_name=f'survey_{st.session_state["access_key"]}.json',
            mime='text/json',
        )
        # Check if the checkbox is selected
        dev_mode = st.checkbox('Developer Mode')

        if dev_mode:
            st.json(st.session_state)
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
            
            st.write(survey)

# Run the app
if __name__ == "__main__":
    main()

