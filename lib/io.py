import streamlit as st
from st_supabase_connection import SupabaseConnection
import streamlit_survey as ss
from streamlit_extras.row import row
from lib.geo import reverse_lookup
from datetime import datetime
from lib.texts import friendly_time

conn = st.connection("supabase", type=SupabaseConnection)

def create_button(key, kwargs = {}):
    return st.button(label=key)

def create_dichotomy(key, kwargs = {}):
    survey = kwargs.get('survey')
    label = kwargs.get('label', 'Confidence')
    name = kwargs.get('name', 'there')
    title = kwargs.get('title', 'Your choice')
    question = kwargs.get('question', 'Dychotomies, including time...')
    messages = kwargs.get('messages', ["🖤", "Meh. Balloons?", "... in between ..."])
    inverse_choice = kwargs.get('inverse_choice', lambda x: x)
    _response = kwargs.get('response', '## You can always change your mind. Now, to the next step.')
    col1, col2, col3 = st.columns([3, .1, 1])
    with col1:    
        response = survey.dichotomy(name=name, 
                                label=label,
                                question=question,
                                height = kwargs.get('height', 100),
                                gradientWidth = kwargs.get('gradientWidth', 30), 
                                key=key)
    with col3:
        if response:
            st.markdown('\n')            
            st.markdown(f'## {title}:', unsafe_allow_html=True)
            st.markdown(f'## {inverse_choice(float(response))}')
            st.markdown(f'{float(response)}', unsafe_allow_html=True)
            if float(response) < 0.1:
                st.warning(messages[0])
            if float(response) > 0.9:
                st.info(messages[1])
            elif 0.1 < float(response) < 0.9:
                st.success(messages[2])
        else:
            st.markdown(f'## Take your time:', unsafe_allow_html=True)
    if response:
        st.markdown(_response)
    
    return response

def create_dichotomy_with3cols(key, kwargs = {}):
    return create_dichotomy(key, kwargs)

def create_qualitative(key, kwargs = {}):
    survey = kwargs.get('survey')
    return survey.qualitative_parametric(name="Spirit",
            question = "Support, Donate, or Invest?",
            label="Qualitative",
            areas = 3,
            key = "parametric")

def create_yesno(key, kwargs = {}):
    survey = kwargs
    callback_yes, callback_no = kwargs.get('callback', (lambda: None, lambda: None))
    col1, col2 = st.columns(2)
    with col1:
        yes_clicked = st.button("Yes", key=f"{key}_yes", on_click=callback_yes)
    with col2:
        no_clicked = st.button("No", key=f"{key}_no", on_click=callback_no)
    
    return

def create_yesno_row(key, kwargs = {}):
    survey = kwargs.get('survey')
    callback_yes, callback_no = kwargs.get('callback', (lambda: None, lambda: None))
    label_no, label_yes = kwargs.get('labels', ('Yes', 'No'))
    
    links_row = row(2, vertical_align="center")
    links_row.button(
        label_yes,
        use_container_width=True,
        on_click = callback_no,
        key=f"{key}_no",
    )

# ""
# ""
    links_row.button(
        label_no,
        use_container_width=True,
        on_click = callback_yes,
        key=f"{key}_yes",
    )

def create_next(key, kwargs = {}):
    survey = kwargs
    return st.button("Next", key=f"{key}")

def create_globe(key, kwargs = {'database': 'gathering', 'table': 'gathering'}):

    data = fetch_and_display_data(conn, kwargs)
    
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
    
    return 

def create_textinput(key, kwargs = {}):
    survey = kwargs.get('survey')
    text = survey.text_input(key, help="Help us best route your current location")
    
    location = st.session_state.coordinates
    
    # if location:
    #     with st.spinner():
    #         _lookup = reverse_lookup(st.secrets.opencage["OPENCAGE_KEY"], location)
    
    #     data = _lookup
    #     # # Access relevant information from the first entry
    #     first_entry = data[0][0]
    #     # political_union = first_entry["components"]["political_union"]
    #     print(first_entry["annotations"]["sun"]["rise"])
    #     sun_rise = first_entry["annotations"]["sun"]["rise"]["astronomical"]
    #     sun_set = first_entry["annotations"]["sun"]["set"]["astronomical"]
    #     print(str(list(first_entry["annotations"]["UN_M49"]["regions"])[-2]).lower())
    #     geographical_region = str(list(first_entry["annotations"]["UN_M49"]["regions"])[-2]).title()
    #     confidence = first_entry["confidence"]
    #     st.markdown(f"### The Sun rises from the east and sets in the west.")
    # #     st.markdown(f"## The geographical region is {geographical_region} and the political union is {political_union}.")
    #     st.markdown(f"## Our confidence in  level is {confidence}.")
    #     sun_rise_readable = datetime.utcfromtimestamp(sun_rise).strftime('%H:%M:%S UTC')
    #     sun_set_readable = datetime.utcfromtimestamp(sun_set).strftime('%H:%M:%S UTC')

    #     st.markdown(f"In {text}, the sun rises at {friendly_time(sun_rise)} and sets at {friendly_time(sun_set)}.")
    #     # st.markdown(f"The sun rises at {sun_rise_readable} and sets at {sun_set_readable} in {text}.")


    #     st.markdown(f"## Forward, confirming that you connect from `{geographical_region}`")

def create_checkbox(key, kwargs = {'label': 'Choose'}):
    survey = kwargs.get('survey')
    return survey.checkbox(kwargs.get('label', ''), key=key)

def create_equaliser(key, kwargs={}):
    survey = kwargs.get('survey')
    rows = 1
    dimensions = kwargs["data"]
    split_len = len(dimensions) // rows
    bottom_cols = st.columns(split_len)

    # for j in range(rows):
    j = 0
    with st.container():
        for i, column in enumerate(bottom_cols):
            with column:
                survey.equaliser(
                    label=dimensions[i + j*split_len][0],
                    height=200,
                    key=f"cat_{i}_{j}",
                    default_value = 0,
                    step=1,
                    min_value=0,
                    slider_color=('red','white'),
                    thumb_shape="circle",
                    max_value=100,
                    value_always_visible=True,
                )

def fetch_and_display_data(conn, kwargs):
    # Fetch all data from the "questionnaire" table
    table_name = kwargs.get('database')
    st.write(f"Fetching data from the {table_name} table.")
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
        st.write(f"No data found in the {table_name} table.")
    return _data

import streamlit as st
import json

class QuestionnaireDatabase:
    def __init__(self, conn, table_name="questionnaire"):
        self.conn = conn
        self.table_name = table_name

    def check_existence(self, key, key_label = 'signature'):
        if key == "":
            st.error("Please provide a key.")
            return

        # Check if the username already exists
        user_exists, count = self.conn.table(self.table_name) \
            .select("*") \
            .ilike(key_label, f'%{key}%') \
            .execute()

        return len(user_exists[1]) > 0

    def insert_data(self, key, key_label, data, data_label = 'response_data'):
        # Insert the data into the PostgreSQL table
        api = self.conn.table(self.table_name)
        api.upsert([
            {key_label: key, data_label: data}
        ]).execute()
        st.write("Data stored in the table.")

    def insert_or_update_data(self, username, data):
        try:
            user_exists = self.check_existence(username.get('key'), username.get('label'))

            if user_exists:
                data = {data.get('label', 'data'): json.dumps(data.get('record'))}
                # Username exists, update the existing record
                update_query = self.conn.table(self.table_name).update(data).eq(username.get('label'), 
                                                                                username.get('key')).execute()
                
                if update_query:
                    st.success(f"Data updated successfully.")
                else:
                    st.error("Failed to update data.")
            else:
                # Username does not exist, insert a new record
                # data = {'name': username, 'data': json.dumps(data)}
                data = {username.get('label'): username.get('key'), 
                        data.get('label', 'data'): json.dumps(data.get('record'))}
                # st.write(data)
                insert_result = self.conn.table(self.table_name).upsert(data).execute()
                st.info("Username does not exist, yet. Yet, accounted for preferences")
        except Exception as e:
            st.error(f"Error inserting or updating data in the database: {str(e)}")


    def fetch_data(self, kwargs = {}):
        # Fetch all data from the "questionnaire" table
        if kwargs.get('verbose', False):
            st.write(f"Fetching data from the {self.table_name} table.")
        response = self.conn.table(self.table_name).select("*").execute()
        # st.write(response)
        if response and response.data:
            data = response.data
            _data = []
            # Display each row of data
            for row in data:
                _data.append(row)
        else:
            st.write(f"No data found in the {self.table_name} table.")
        return _data

# Usage example:
# db = QuestionnaireDatabase(conn)
# db.insert_or_update_data(username, response_data)
