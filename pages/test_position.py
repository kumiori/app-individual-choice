import streamlit as st
import streamlit_survey as ss


if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Positioning Portal",
        page_icon="✨",
        layout="wide",
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


from pages.test_location import conn

from pages.test_1d import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from streamlit_extras.streaming_write import write as streamwrite 
import time
from pages.test_stream import _stream_once
import json
import hashlib

st.write(st.secrets["runtime"]["STATUS"])

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

def fetch_and_display_data(conn, table_name = "gathering"):
    # Fetch all data from the "questionnaire" table
    response = conn.table(table_name).select("*").execute()
    # st.write(response)
    # Check if there is any data in the response
    if response and response.data:
        data = response.data
        _data = []
        # Display each row of data
        for row in data:
            # st.write(row)
            # st.write(f"Username: {row['name']} Id: {row['id']} timestamp: {row['created_at']}")
            # st.json(json.loads(row['response_data']))
            _data.append({"lat": row["latitude"], "lng": row["longitude"], "luckynumber": row["luckynumber"]+1})
            # st.write("------------")
    else:
        st.write("No data found in the 'questionnaire' table.")
    return _data

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


def main():
    # st.title("Welcome to the Singular Mapping. A solid proof? Forget, and Ask the moon: If If-Then is full, is still Luck a useful tool? \n ## We divide by zero. \n ## and it's just fuck*ng pitch black..")
    title = """
    ## This is the Singular Mapping. 
    # A solid proof? 
    ### Forget, and ask the Moon: ... 

    # &quot; If If-Then is full, is still Luck afoot just...as a tool?&quot; 0/0. 
    ## (what if) We divide by zero... \n ## and it's just fuck*ng pitch black..

    """
    stream = st.empty()
    with stream:
        _stream, errors = corrupt_string(title, damage_parameter=0.0)
        st.title(f"System errors number {errors}")
        streamwrite(_stream_once(_stream, damage=0.5), unsafe_allow_html=True)
        with st.spinner('...'):
            time.sleep(3)
        streamwrite(_stream_once("## The Moon will still be able to see you...", damage=0.), unsafe_allow_html=True)

    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter

    col1, col2, col3 = st.columns(3)

    survey = ss.StreamlitSurvey("The Where?")

    with col2:
        st.markdown("## ¿ What is your")
        location = survey.text_input("location", help="Our location will appear shortly...", value=st.session_state.location)
    
    if location is not None:
        coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
        st.session_state.coordinates = coordinates
        
        with col1:
            st.markdown("## As a rule of thumb...")
            
        with col3:
            st.markdown("## Luck (y)")
            lucky_number = survey.number_input("number", min_value=0, max_value=1000000000)

        # if col3.button("\>"):
        #     st.info("Next is showing the whole")


        # Send Data Button
        if col1.button("Claim your place/Check in"):
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
                st.success(f"This is your signature \n`` {signature} ``. Keep it in your files, it will allow swift access to the past.")
            else:
                _default = data["location"]+"-"+str(data["luckynumber"])
                access = survey.text_input("signature", help="Your fingerprint.")
                
        
        col1, col3, col3 = st.columns(3) 
                       
        if hasattr(st.session_state, 'coordinates'):
            if col2.button("Display our Map"):
                data = fetch_and_display_data(conn, table_name="gathering")
                
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

