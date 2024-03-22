# Streamlit Timeline Component Example

import streamlit as st
from streamlit_timeline import timeline
import json
import datetime

# use full page width
st.set_page_config(page_title="Settimia's Timeline", layout="wide")

# load data
# with open('example.json', "r") as f:
#     data = f.read()


data = {
    "title": {
        "media": {
          "url": "",
          "caption": " <a target=\"_blank\" href=''>credits</a>",
          "credit": ""
        },
        "text": {
          "headline": "Welcome to<br>Streamlit Timeline",
          "text": "<p>A Streamlit Timeline component by integrating TimelineJS from Knightlab</p>"
        }
    },
    "events": [
      {
        "media": {
          "url": "https://vimeo.com/143407878",
          "caption": "How to Use TimelineJS (<a target=\"_blank\" href='https://timeline.knightlab.com/'>credits</a>)"
        },
        "start_date": {
          "year": "2016",
          "month":"1"
        },
        "text": {
          "headline": "TimelineJS<br>Easy-to-make, beautiful timelines.",
          "text": "<p>TimelineJS is a populair tool from Knightlab. It has been used by more than 250,000 people to tell stories seen hundreds of millions of times, and is available in more than sixty languages. </p>"
        }
      },
      {
        "media": {
          "url": "https://www.youtube.com/watch?v=CmSKVW1v0xM",
          "caption": "Streamlit Components (<a target=\"_blank\" href='https://streamlit.io/'>credits</a>)"
        },
        "start_date": {
          "year": "2020",
          "month":"7",
          "day":"13"
        },
        "text": {
          "headline": "Streamlit Components<br>version 0.63.0",
          "text": "Streamlit lets you turn data scripts into sharable web apps in minutes, not weeks. It's all Python, open-source, and free! And once you've created an app you can use our free sharing platform to deploy, manage, and share your app with the world."
        }
      },
      {
        "media": {
          "url": "https://github.com/innerdoc/streamlit-timeline/raw/main/component-logo.png",
          "caption": "github/innerdoc (<a target=\"_blank\" href='https://www.github.com/innerdoc/'>credits</a>)"
        },
        "start_date": {
          "year": "2021",
          "month":"2"
        },
        "text": {
          "headline": "Streamlit TimelineJS component",
          "text": "Started with a demo on https://www.innerdoc.com/nlp-timeline/ . <br>Then made a <a href='https://github.com/innerdoc/streamlit-timeline'>Streamlit component</a> of it. <br>Then made a <a href='https://pypi.org/project/streamlit-timeline/'>PyPi package</a> for it."
        }
      }
    ]
}

# load data

# with open('pages/timeline_example.json', "r") as f:
#     data = f.read()

current_year = datetime.datetime.now().year

data = {
    "title": {
        "media": {
            "url": "",
            "caption": " <a target=\"_blank\" href=''>credits</a>",
            "credit": ""
        },
        "text": {
            "headline": "Settimia's Timeline",
            "text": "<p>A timeline with events (large and small), workshops, and an auction.</p>"
        }
    },
    "events": [
        {
            "media": {
                "url": "",
                "caption": "Major Event 1"
            },
            "start_date": {
                "year": str(current_year),
                "month": "3",
                "day": "30"
            },
            "text": {
                "headline": "Settimia Hosts: Call it Easter",
                "text": "<p>Andrew's Birthday, The first major event of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Men's Fashion Week (Mi)"
            },
            "start_date": {
                "year": str(current_year),
                "month": "6",
                "day": "15"
            },
            "end_date": {
                "year": str(current_year),
                "month": "6",
                "day": "19"
            },
            "text": {
                "headline": "Men's Fashion Week (Mi)",
                "text": "<p>The first two-week workshop of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Women's Fashion Week (Mi)"
            },
            "start_date": {
                "year": str(current_year),
                "month": "9",
                "day": "18"
            },
            "end_date": {
                "year": str(current_year),
                "month": "9",
                "day": "24"
            },
            "text": {
                "headline": "Women's Fashion Week (Mi)",
                "text": "<p>The first two-week workshop of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Major Event 2"
            },
            "start_date": {
                "year": str(current_year),
                "month": "4",
                "day": "1"
            },
            "text": {
                "headline": "Major Event 2",
                "text": "<p>The second major event of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Two-Week Workshop 2"
            },
            "start_date": {
                "year": str(current_year),
                "month": "6",
                "day": "1"
            },
            "end_date": {
                "year": str(current_year),
                "month": "6",
                "day": "14"
            },
            "text": {
                "headline": "Two-Week Workshop 2",
                "text": "<p>The second two-week workshop of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Major Event 3"
            },
            "start_date": {
                "year": str(current_year),
                "month": "8",
                "day": "1"
            },
            "text": {
                "headline": "Major Event 3",
                "text": "<p>The third major event of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Auction"
            },
            "start_date": {
                "year": str(current_year),
                "month": "10",
                "day": "1"
            },
            "text": {
                "headline": "Auction",
                "text": "<p>An auction event in the tenth month of the year.</p>"
            }
        },
        {
            "media": {
                "url": "",
                "caption": "Major Event 4"
            },
            "start_date": {
                "year": str(current_year),
                "month": "12",
                "day": "1"
            },
            "text": {
                "headline": "Major Event 4",
                "text": "<p>The fourth major event of the year.</p>"
            }
        }
    ]
}
# render timeline
timeline(data, height=800)