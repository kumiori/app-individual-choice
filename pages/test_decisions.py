import json
import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from streamlit_elements import dashboard, elements, html, mui, nivo


cols = st.columns(3)
st.markdown("# Decision trees")

layout = [
    # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
    dashboard.Item("first_item", 0, 0, 1, 1),
    dashboard.Item("second_item", 1, 0, 1, 1, isDraggable=False, moved=False),
    dashboard.Item("third_item", 2, 0, 1, 1, isDraggable=True, isResizable=False),
    dashboard.Item("fourth_item", 3, 0, 1, 1, isDraggable=False, isResizable=False),
]

with elements("nivo_charts"):

    DATA = [
    {
        "id": "yes",
        "label": "Yes",
        "value": 12
    },
    {
        "id": "uncertain",
        "label": "Uncertain",
        "value": 3
    },
    {
        "id": "nos",
        "label": "No",
        "value": 1
    }
    ]
    with mui.Box(sx={"height": 300}):
        nivo.Waffle(
            data=DATA,
            total=40,
            rows=18,
            columns=14,
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
