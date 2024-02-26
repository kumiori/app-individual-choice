import streamlit as st

import random

if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Celestial Verse Portal",
        page_icon="✨",
        # layout="wide",
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
else:
    st.set_page_config(
        # layout="wide",
        initial_sidebar_state="collapsed"
        )



patriarchy_screams = """
# Patriarchy screams for help because &hellip;.

# Patriarchy shouts &hellip; because &hellip;.

# Patriarchy yells &hellip; because &hellip;.

# Patriarchy howls &hellip; because &hellip;.

# Patriarchy roars &hellip; because &hellip;.

# Patriarchy whispers &hellip; because &hellip;.

# Patriarchy murmurs &hellip; because &hellip;.

# Patriarchy mumbles &hellip; because &hellip;.

# Patriarchy mutters &hellip; because &hellip;.

# Patriarchy grumbles &hellip; because &hellip;.

# Patriarchy groans &hellip; because &hellip;.

# Patriarchy moans &hellip; because &hellip;.

# Patriarchy whimpers &hellip; because &hellip;.

# Patriarchy whines &hellip; because &hellip;.

# Patriarchy squeals &hellip; because &hellip;.

# Patriarchy squeaks &hellip; because &hellip;.

# Patriarchy squawks &hellip; because &hellip;.

# Patriarchy screechs &hellip; because &hellip;.

# Patriarchy shrieks &hellip; because &hellip;.

# Patriarchy yelps &hellip; because &hellip;.

# Patriarchy yowls &hellip; because &hellip;.

# Patriarchy bellows &hellip; because &hellip;.

# Patriarchy bawls &hellip; because &hellip;.

# Patriarchy blubbers &hellip; because &hellip;.

# Patriarchy blurts &hellip; because &hellip;.

# Patriarchy blurts out &hellip; because &hellip;.

# Patriarchy blabs &hellip; because &hellip;.

# Patriarchy blabbers &hellip; because &hellip;.

# Patriarchy babbles &hellip; because &hellip;.

# Patriarchy gabbles &hellip; because &hellip;.

# Patriarchy gibbers &hellip; because &hellip;.

# Patriarchy jabbers &hellip; because &hellip;.

# Patriarchy patters &hellip; because &hellip;.

# Patriarchy prattles &hellip; because &hellip;.

# Patriarchy rambles &hellip; because &hellip;.

# Patriarchy maunders &hellip; because &hellip;.

# Patriarchy drivels &hellip; because &hellip;.

# Patriarchy drools &hellip; because &hellip;.

# Patriarchy slobbers &hellip; because &hellip;.

# Patriarchy slavers &hellip; because &hellip;.

# Patriarchy slabbers &hellip; because &hellip;.

# Patriarchy dribbles &hellip; because &hellip;.

# Patriarchy dabbles &hellip; because &hellip;.

# Patriarchy dawdles &hellip; because &hellip;.

# Patriarchy dallys &hellip; because &hellip;.

# Patriarchy dillys-dally for because &hellip; help.
# Patriarchy lingers &hellip; because &hellip;.

# Patriarchy loiters &hellip; because &hellip;.

# Patriarchy tarrys &hellip; because &hellip;.

# Patriarchy procrastinates &hellip; because &hellip;.

"""

import hashlib
from pages.test_1d import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from streamlit_extras.streaming_write import write as streamwrite 
import time
import string
import streamlit_survey as ss
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
from pages.test_paged import PagedContainer
from pages.test_location import conn
from pages.test_position import fetch_and_display_data

class _PagedContainer(PagedContainer):
    def display_page(self, page):
        # start_idx = self.current_page * self.items_per_page
        start_idx = page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        # page_items = self.items[start_idx:end_idx]
        page_items = [start_idx, end_idx]
        # print(page_items)
        display_dictionary_by_indices(self.items, indices=page_items)
        # for item in page_items:
            # st.write(item)
        
        st.write(f"Page {page + 1}/{self.get_total_pages()}")

if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Celestial Verse Portal",
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

st.write(st.secrets["runtime"]["STATUS"])

# Initialize read_texts set in session state if not present
if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def _stream_once(text, damage):
    text_hash = hash_text(text)

    # Define sleep lengths for different punctuation symbols
    sleep_lengths = {'.': 1., ',': 0.3, '!': 1.7, '?': 1.5, ';': 0.4, ':': 0.4}
    sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}
    # st.json(sleep_lengths)

    # st.write(sleep_lengths.values() * (1+damage))

    # Check if the text has already been read
    if text_hash not in st.session_state.read_texts:
        # st.write(text)
    
        for i, word in enumerate(text.split()):
            # Check if the last character is a punctuation symbol
            last_char = word[-1] if word[-1] in string.punctuation else None

            # Yield the word with appropriate sleep length
            if last_char == '.' or last_char == '?' or last_char == '^':
                yield word + " \n "
            else:
                yield word + " "
            
            if last_char and last_char in sleep_lengths:
                time.sleep(sleep_lengths[last_char])
            else:
                time.sleep(0.3)
            
        st.session_state.read_texts.add(text_hash)  # Marking text as read

def create_streamed_columns(panel):
    num_panels = len(panel)
    
    for i in range(num_panels):
        width_pattern = [2, 1] if i % 2 == 0 else [1, 2]
        cols = st.columns(width_pattern)

        col_idx = 0  if i % 2 == 0 else 1
        with cols[col_idx]:
            streamwrite(_stream_once(panel[i], 0))

# Usage



def match_input(input_text, translation_dict):
    matching_keys = [key for key, value in translation_dict.items() if value.lower() == input_text.lower()]

    if matching_keys:
        return matching_keys
    else:
        return False

intro_text = """
## Our questions are simple.
"""

panel_1 = """ ## I ... '_aptriarhcy'_.""" 

panel_2 = """## These .... as much in their effects as in their causes. 
"""

"""think of a stimulating game, role play, that rewards
    do you see youself? who are you, siren, pope, rockstar
    how would you like to play? what would you like to play?
    
    shot: cards plus tit nipple    

    focus on: (equaliser)  
    - social aspects
    - mystic rituals
    - introspection
    - sexual freedom
    - economic affairs

    Returns:
        _type_: _description_
        
    What matters is your voice, here and now.
    Take one breadth or two, to commit to yourself
    to free space of mind, not a password to remind
    the reminder is for you, check again
    look forward, in time
    
    your time
    your location
    your power
    
    unlock the door
    check in again in a few days
    
    your access key: md5(_sign(location, time))

    map: username: access key
    password: hash(power)
"""
panel = [panel_1, panel_2]

# Main function
def main():
    # Page title
    # st.title(":tent: Reflecting :moon: with the Moon :sparkles:")
    st.title(":circus_tent: _Mes dames et mes soeurs*_ :eyes:")
    st.title(":circus_tent: Patriarchy is under scrutiny :eyes:")
    # st.markdown("## How do you feel? Really, do you feel it? Does it affect, does it touch? Does it look good, as a portrait?")
    st.markdown("### *) Ladies and sisters")
    
    # Session State also supports attribute based syntax
    survey = ss.StreamlitSurvey("Home")
    col1, col2, col3 = st.columns(3)


        # creates an current_page element in session_state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 0
    
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    if 'damage_parameter' not in st.session_state:
        st.session_state.damage_parameter = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.coordinates = None  # Initial damage parameter

    survey = ss.StreamlitSurvey("Home")
    st.write(f'page_number {st.session_state.page_number}')

    # once usage:
    streamwrite(_stream_once(intro_text, 0))
    st.write(st.session_state.read_texts)
    
    col1, _, col2 = st.columns([3, 0.1, 1])
    with col1:
        st.markdown("## Are you happy...to play?")
        st.markdown('No is \'no\'.')
    with col2:
        response = survey.text_input("Try to respond in your natural language...", help="Our location will appear shortly...", value="")
        # result = match_input(response, yesses)
        st.write(response)
    

    create_streamed_columns(panel)    

def display_category_description(sup_category, category, description):
    """
    Function to display category and its description.
    """
    col0, col1, col2 = st.columns([1, 1, 2])
    with col0:
        st.write(f"## **{sup_category}**")

def display_details_description(category, details):
    """
    Function to display category and its description.
    """
    col0, col1, col2 = st.columns([3, 3, 3])
    with col0:
        st.write(f"## **{category}**")
    for sub_category, description in details.items():
        with col1:
            st.write(f"## **{sub_category}**")
        with col2:
            st.write(f" **{description}**")
            st.write("---")

def display_patriarchy_dimensions(patriarchy_dimensions):
    """
    Function to display the data contained in patriarchy_dimensions.
    """
    for category, details in patriarchy_dimensions.items():
        st.markdown(f"## **{category}**")
        for sub_category, description in details.items():
            display_category_description(category, sub_category, description)

def display_dictionary_by_indices(dictionary, indices=None):
    """
    Function to display the data contained in dictionary for a specified subset using indices.
    """
    categories = list(dictionary.keys())
    if indices is None:
        indices = range(len(categories))
    else:
        indices = sorted(set(indices))  # Ensure uniqueness and sort the indices

    for idx in range(indices[0], indices[1]):
        if 0 <= idx < len(categories):
            category = categories[idx]
            details = dictionary.get(category, {})
            display_details_description(category, details)
            # for sub_category, description in details.items():
                # display_category_description(category, sub_category, description)

if __name__ == "__main__":
    main()
    # add_vertical_space(1)
    survey = ss.StreamlitSurvey("Home")
    
    st.markdown("#### Play more")
    links_row = row(2, vertical_align="center")
    links_row.button(
        ":honey_pot: Explore our panel contributions",
        use_container_width=True,
    )
    links_row.link_button(
        ":ticket:  Visit the conference's website",
        "https://www.europeindiscourse.eu/",
        use_container_width=True,
    )
    from  streamlit_vertical_slider import vertical_slider 

    st.markdown("## Energetic Equaliser")
        
    patriarchy_dimensions = {
        'Economic Disparities': {
            'Wage Gap': 'Persistent gender wage gap in which women earn less for the same work.',
            'Occupational Segregation': 'Women often clustered in lower-paying and undervalued professions.'
        },
        'Gendered Social Roles': {
            'Traditional Expectations': 'Societal norms dictating gendered roles and expectations for women.',
            'Motherhood Penalty': 'Professional setbacks for women due to biases related to motherhood.'
        },
        'Reproductive Rights and Health': {
            'Limited Access to Healthcare': 'Challenges in accessing comprehensive healthcare, including reproductive health services.',
            'Reproductive Rights': 'Ongoing debates surrounding reproductive rights, including access to contraception and abortion.'
        },
        'Violence and Harassment': {
            'Gender-Based Violence': 'Women facing various forms of gender-based violence, including domestic violence, sexual assault, and harassment.',
            'Workplace Harassment': 'Harassment in professional settings hindering women\'s professional growth.'
        },
        'Media and Cultural Influences': {
            'Objectification': 'Media perpetuating the objectification of women, reinforcing harmful beauty standards.',
            'Stereotyping': 'Gender stereotypes in media limiting women\'s representation and perpetuating narrow portrayals.'
        },
        'Political Under-representation': {
            'Gender Disparities in Leadership': 'Women underrepresented in political leadership roles.',
            'Policy Biases': 'Policies influenced by male-dominated perspectives may not adequately address women\'s challenges.'
        },
        'Intersectionality': {
            'Overlapping Oppressions': 'Recognition that the impact of patriarchy intersects with other forms of oppression.'
        }
    }
    dimensions =  {"social aspects",
    "mystic rituals",
    "introspection",
    "sexual freedom",
    "economic affairs"}
# dualité sexué que le aptr instaure
# heterosexuelle et sexiste, 
# la 
# Example: Accessing data
    # st.write(f'session {st.session_state}')
    paged_container = _PagedContainer(patriarchy_dimensions)
    # print(patriarchy_dimensions.keys())
    bottom_cols = st.columns(len(dimensions))
    
    for column, category in zip(bottom_cols, dimensions):
        with column:
            vertical_slider(
                label=category,
                height=200,
                key=category,
                default_value=random.random() * 100,
                step=1,
                min_value=0,
                max_value=100,
                value_always_visible=True,
            )
    

    with st.expander("Patriarchy Dimensions"):
        col1, _, col2 = st.columns([2, 10, 2])
        with col2:
            if st.button("Next"):
                st.session_state["current_page"] = min(st.session_state.current_page + 1, paged_container.get_total_pages() - 1)
        with col1:
            if st.button("Prev"):
                st.session_state["current_page"] = max(st.session_state.current_page - 1, 0)

        paged_container.display_page(st.session_state.current_page)
        

    st.write(
        """<style>
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    # Question 2 in the second column
    with col1:  
        st.markdown("## Visible?")
    with col2:
        location = survey.text_input("Location", help="Our location.", value=st.session_state.location)   

    # Question 3 and 4 in the third column
    with col3:
        # birthplace = survey.text_input("Where were you born?", help="Enter the name of your birthplace.")
        power_number = survey.number_input("Lucky number?", min_value=0, max_value=100000000)

    
    if location is not None:
        coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
        if coordinates:
            st.write(f"Coordinates for {location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
            st.session_state.location = location
            st.session_state.coordinates = coordinates
                

    col1, col3, col3 = st.columns(3)
    st.json(st.session_state, expanded=True)
    if hasattr(st.session_state, 'coordinates'):
        if col1.button("Display our Map"):
            data = fetch_and_display_data(conn)

            stream = st.empty()
            # with stream:
                # streamwrite(_stream_example(potentials, damage=0.), unsafe_allow_html=True)

            stream.empty()
            stream.markdown("# This is how the moon sees the planet revolving...")
            stream.markdown("# This is another vodoo need•le on the patriarchal world...")

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
            
            streamwrite(_stream_once(patriarchy_screams, 0))
            
    # display_patriarchy_dimensions(patriarchy_dimensions)

    # with bottom_cols[0]:
    #     tst = vertical_slider(
    #         label="Default Style",
    #         height=200,
    #         key="test_0",
    #         default_value=55,
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )

    # with bottom_cols[1]:
    #     tst = vertical_slider(
    #         label="Default Style + Always Visible",
    #         height=200,
    #         key="test_1",
    #         default_value=55,
    #         thumb_shape="circle",
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )

    # with bottom_cols[2]:
    #     tst = vertical_slider(
    #         label="Pill Shaped",
    #         height=200,
    #         key="test_2",
    #         default_value=55,
    #         thumb_shape="pill",
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )

    # with bottom_cols[3]:
    #     tst = vertical_slider(
    #         label="Square Shaped",
    #         height=200,
    #         key="test_3",
    #         default_value=55,
    #         thumb_shape="square",
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )

    # with bottom_cols[4]:
    #     tst = vertical_slider(
    #         label="Custom Colors",
    #         thumb_color="Red",
    #         track_color="gray",
    #         slider_color="orange",
    #         height=200,
    #         key="test_4",
    #         default_value=55,
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )

    # with bottom_cols[5]:
    #     tst = vertical_slider(
    #         label="Height Control",
    #         height=200,
    #         key="test_5",
    #         default_value=55,
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )

    # with bottom_cols[6]:
    #     tst = vertical_slider(
    #         label='asd',
    #         height=200,
    #         key="test_6",
    #         default_value=55,
    #         step=1,
    #         min_value=0,
    #         max_value=100,
    #         value_always_visible=True,
    #     )


# you are getting ready for the next game

# forgot anything? go forward, because you can't go back


# 

#  how it originated? how it is maintained? how it is perpetuated? how it is challenged? how it is dismantled?
 
#   How does it transition? How does it transform? How does it evolve? How does it adapt? How does it chang
  
#    how it has transitioned to this stage? How can it be nudged? How can it be perturbed?
   
#     We take constructive approach in the analysis of power structures starting to understand how they feel individually, what energies they are allowed to express, what forces do they rely upon?
    
#     Let's test the logic and the assumptions of the power structures. Let's see how they feel. Let's see how they think. Let's see how they behave. Let's see how they react. Let's see how they respond. Let's see how they adapt. Let's see how they evolve. Let's see how they transform. Let's see how they transition. Let's see how they change. Let's see how they shift. Let's see how they move. Let's see how they flow. Let's see how they grow. Let's see how they expand. Let's see how they contract. Let's see how they oscillate. Let's see how they vibrate. Let's see how they resonate. Let's see how they radiate. Let's see how they emit. Let's see how they absorb. Let's see how they reflect. Let's see how they refract. Let's see how they diffract. Let's see how they scatter. Let's see how they disperse. Let's see how they disintegrate. Let's see how they dissolve. Let's see how they decay. Let's see how they decompose. Let's see how they break. Let's see how they shatter. Let's see how they crack. Let's see how they split. Let's see how they fragment. Let's see how they crumble. Let's see how they collapse. Let's see how they fall. Let's see how they tumble. Let's see how they roll. Let's see how they slide. Let's see how they glide. Let's see how they slip. Let's see how they drift. Let's see how they wander. Let's see how they stray. Let's see how they deviate. Let's see how they diverge. Let's see how they digress. Let's see how they meander. Let's see how they ramble. Let's see how they roam. Let's see how they rove. Let's see how they range. Let's see how they depart. Let's see how they stray. Let's see how they veer. Let's see how they swerve. Let's see how they turn. Let's see how they curve. Let's see how they bend. Let's see how they flex. Let's see how they twist. Let's see how they warp. Let's see how they distort. Let's see how they buckle. Let's see how they cry for help.
