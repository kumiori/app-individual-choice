import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_elements import mui
from streamlit_elements import nivo
import json
from pathlib import Path

with elements("nivo_charts"):


    DATA = [
        { "taste": "social", "last week": 93, "yesterday": 61, "today": 114 },
        { "taste": "economic", "last week": 91, "yesterday": 37, "today": 72 },
        { "taste": "emotional", "last week": 56, "yesterday": 95, "today": 99 },
        { "taste": "scientific", "last week": 64, "yesterday": 90, "today": 30 },
        { "taste": "musical", "last week": 119, "yesterday": 94, "today": 103 },
    ]

    with mui.Box(sx={"height": 500}):
        nivo.Radar(
            data=DATA,
            # keys=[ "last week", "yesterday", "today" ],
            keys=["yesterday"],
            indexBy="taste",
            valueFormat=">-.2f",
            margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
            borderColor={ "from": "color" },
            gridLabelOffset=36,
            dotSize=10,
            dotColor={ "theme": "background" },
            dotBorderWidth=2,
            motionConfig="wobbly",
            legends=[
                {
                    "anchor": "top-left",
                    "direction": "column",
                    "translateX": -50,
                    "translateY": -40,
                    "itemWidth": 80,
                    "itemHeight": 20,
                    "itemTextColor": "#999",
                    "symbolSize": 12,
                    "symbolShape": "circle",
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemTextColor": "#000"
                            }
                        }
                    ]
                }
            ],
            theme={
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        )

with elements("nivo_charts_line"):
    DATA = [
    {
        "id": "japan",
        "color": "hsl(283, 70%, 50%)",
        "data": [
        {
            "x": "plane",
            "y": 62
        },
        {
            "x": "helicopter",
            "y": 190
        },
        {
            "x": "boat",
            "y": 176
        },
        {
            "x": "train",
            "y": 150
        },
        {
            "x": "subway",
            "y": 40
        },
        {
            "x": "bus",
            "y": 38
        },
        {
            "x": "car",
            "y": 1
        },
        {
            "x": "moto",
            "y": 278
        },
        {
            "x": "bicycle",
            "y": 31
        },
        {
            "x": "horse",
            "y": 158
        },
        {
            "x": "skateboard",
            "y": 267
        },
        {
            "x": "others",
            "y": 57
        }
        ]
    },
    ]

    with mui.Box(sx={"height": 200}):
        nivo.Line(
            data=DATA,
        )

with elements("nivo_charts_bump"):
    DATA = [
        {
            "id": "Serie 1",
            "data": [
            {
                "x": "2000",
                "y": 11
            },
            {
                "x": "2001",
                "y": 5
            },
            {
                "x": "2002",
                "y": 10
            },
            {
                "x": "2003",
                "y": 9
            },
            {
                "x": "2004",
                "y": 8
            }
            ]
        },
        {
            "id": "Serie 2",
            "data": [
            {
                "x": "2000",
                "y": 7
            },
            {
                "x": "2001",
                "y": 3
            },
            {
                "x": "2002",
                "y": 11
            },
            {
                "x": "2003",
                "y": 12
            },
            {
                "x": "2004",
                "y": 5
            }
            ]
        },
        {
            "id": "Serie 3",
            "data": [
            {
                "x": "2000",
                "y": 10
            },
            {
                "x": "2001",
                "y": 4
            },
            {
                "x": "2002",
                "y": 1
            },
            {
                "x": "2003",
                "y": 3
            },
            {
                "x": "2004",
                "y": 11
            }
            ]
        },
        ]

    with mui.Box(sx={"height": 500}):
        nivo.Bump(
            data=DATA,
            colors={ "scheme": "spectral" },
            lineWidth=3,
            activeLineWidth=6,
            inactiveLineWidth=3,
            inactiveOpacity=0.15,
            pointSize=10,
            activePointSize=16,
            inactivePointSize=0,
            pointColor={ "theme": "background" },
            pointBorderWidth=3,
            activePointBorderWidth=3,
            pointBorderColor={ "from": "serie.color" },
            axisTop={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "",
                "legendPosition": "middle",
                "legendOffset": -36
            },
            axisBottom={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "",
                "legendPosition": "middle",
                "legendOffset": 32
            },
            axisLeft={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "ranking",
                "legendPosition": "middle",
                "legendOffset": -40
            },
            margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
            axisRight=None,
        )
        

with elements("nivo_charts_bump_presence"):
    
    with mui.Box(sx={"height": 500}):
        nivo.Bump(
            data=json.loads(Path('data/presence_data.json').read_text()),
            colors={ "scheme": "spectral" },
            lineWidth=3,
            activeLineWidth=6,
            inactiveLineWidth=3,
            inactiveOpacity=0.15,
            pointSize=10,
            activePointSize=16,
            inactivePointSize=0,
            pointColor={ "theme": "background" },
            pointBorderWidth=3,
            activePointBorderWidth=3,
            pointBorderColor={ "from": "serie.color" },
            axisTop={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "",
                "legendPosition": "middle",
                "legendOffset": -36
            },
            axisBottom={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "",
                "legendPosition": "middle",
                "legendOffset": 32
            },
            axisLeft={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "ranking",
                "legendPosition": "middle",
                "legendOffset": -40
            },
            margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
            axisRight=None,
        )