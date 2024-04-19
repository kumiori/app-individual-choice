import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.subplots as sp
from lib.survey import CustomStreamlitSurvey
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase

cols = st.columns(4)
db = IODatabase(conn, "access_keys")

data = db.fetch_data()
df = pd.DataFrame(data)

item_count = len(df)

with cols[0]:
    ui.metric_card(title="Total count", content=item_count, description="Access keys delivered.", key="card1")
with cols[1]:
    ui.metric_card(title="Total GAME", content="0 €", description="Since  _____ we start", key="card2")
with cols[2]:
    ui.metric_card(title="Pending invites", content="1", description="Matteo Zuretti", key="card3")
with cols[3]:
    st.markdown("### Writing")
    ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")
    ui.badges(badge_list=[("production", "primary")], class_name="flex gap-2", key="viz_badges3")
    
# df['created_at'] = pd.to_datetime(df['created_at'])

survey = CustomStreamlitSurvey()

def create_dichotomy(key, kwargs = {}):
    survey = kwargs.get('survey')
    label = kwargs.get('label', 'Confidence')
    name = kwargs.get('name', 'there')
    index = kwargs.get('index', -1)
    question = kwargs.get('question', 'Dychotomies, including time...')
    # question += f' {index}'
    messages = kwargs.get('messages', ["🖤", "Meh. Balloons?", "... in between ..."])
    inverse_choice = kwargs.get('inverse_choice', lambda x: x)
    _response = kwargs.get('response', '## You can always change your mind. Now, to the next step.')
    col1, col2, col3 = st.columns([3, .1, 1])
    callable = kwargs.get('callback')
    
    # with col1:    
    response = survey.dichotomy(name=name, 
                                label=label,
                                question=question,
                                height = kwargs.get('height'),
                                gradientWidth = kwargs.get('gradientWidth', 30), 
                                key=key)
# with col3:    
    if response:
        st.markdown('\n')            
        st.markdown(f'## Your choice:', unsafe_allow_html=True)
        st.markdown(f'## {inverse_choice(float(response))}')
        st.markdown(f'{float(response)}', unsafe_allow_html=True)
        if float(response) < 0.1:
            st.success(messages[0])
        if float(response) > 0.9:
            st.info(messages[1])
        elif 0.1 < float(response) < 0.9:
            st.success(messages[2])
    else:
        st.markdown(f'## Take your time 🛁', unsafe_allow_html=True)

    st.write(*kwargs.get('args', []), response)
    
wrapper = st.empty()

wrapper.image("images/APC_3171.jpg", use_column_width=True)

# col1, col2, col3 = st.columns([1, 5, 1])
# with col2:
response = create_dichotomy(key = "steering", kwargs={'survey': survey,
                                            'label': 'resonance', 
                                            'question': 'White, go forward; black, go back.',
                                            'gradientWidth': 50,
                                            'height': 30,
                                            'inverse_choice': lambda x: '',
                                            'callback': lambda x: st.write(x),}
                            )


embed_gal = "<div class='lr_embed' style='position: relative; padding-bottom: 100%; height: 0; overflow: hidden;'><iframe id='iframe' src='https://lightroom.adobe.com/embed/shares/b26f65ba432d4281a0e12768af1ca8be/slideshow?background_color=%232D2D2D&color=%23999999' frameborder='0'style='width:100%; height:100%; position: absolute; top:0; left:0;' ></iframe></div>"

with st.spinner("Loading..."):
    st.markdown(embed_gal, unsafe_allow_html=True)