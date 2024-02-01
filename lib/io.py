import streamlit as st
from st_supabase_connection import SupabaseConnection
import streamlit_survey as ss

conn = st.connection("supabase", type=SupabaseConnection)

def create_button(key, kwargs = {}):
    return st.button(label=key)

def create_dichotomy(key, kwargs = {}):
    survey = kwargs.get('survey')
    return survey.dichotomy(name="Spirit", 
                            label="Confidence",
                            question="Dychotomies, including time...", 
                            key=key)

def create_qualitative(key, kwargs = {}):
    survey = kwargs
    return survey.qualitative_parametric(name="Spirit",
            question = "Support, Donate, or Invest?",
            label="Qualitative",
            areas = 3,
            key = "parametric")

def create_yesno(key, kwargs = {}):
    survey = kwargs
    col1, col2 = st.columns(2)
    with col1:
        yes_clicked = st.button("Yes", key=f"{key}_yes")
    with col2:
        no_clicked = st.button("No", key=f"{key}_no")
    
    return

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
    text = survey.text_input(key, help="")
    return 

def create_checkbox(key, kwargs = {}):
    survey = kwargs.get('survey')
    return survey.checkbox("Choose one:", key=key)

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

