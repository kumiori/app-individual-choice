import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.subplots as sp

from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase

ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")

cols = st.columns(3)

db = IODatabase(conn, "access_keys")

data = db.fetch_data()
df = pd.DataFrame(data)

item_count = len(df)

with cols[0]:
    ui.metric_card(title="Total count", content=item_count, description="Access keys delivered.", key="card1")
with cols[1]:
    ui.metric_card(title="Total inflow", content="234,300 €", description="Since launched in 2024", key="card2")
with cols[2]:
    ui.metric_card(title="Pending invites", content="712", description="Rank No.1 story of the day", key="card3")

df['created_at'] = pd.to_datetime(df['created_at'])


# Create scatter plot of 'created_at' field
scatter_fig = go.Figure(go.Scatter(x=df['created_at'], y=df.index, mode='markers', name='Scatter Plot of Created At'))
scatter_fig.update_layout(title='Scatter Plot of Created At', xaxis_title='Created At', yaxis_title='Index')

# Create heatmap
heatmap_data = df.groupby([df['created_at'].dt.date]).size().reset_index(name='count')
heatmap_fig = go.Figure(go.Heatmap(x=heatmap_data['created_at'], y=[0], z=[heatmap_data['count']], colorscale='blues'))
heatmap_fig.update_layout(title='Heatmap of Created At', xaxis_title='Date', yaxis_title='', showlegend=False)

# Create subplots
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Scatter Plot", "Heatmap"))
fig.add_trace(scatter_fig.data[0], row=1, col=1)
fig.add_trace(heatmap_fig.data[0], row=1, col=2)

# Update layout
# fig.update_layout(height=600, width=1000)

# Show plots
st.plotly_chart(fig)
