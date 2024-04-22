from streamlit_elements import elements
from streamlit_elements import mui
import streamlit as st

with elements("example_accordion"):
    with mui.Accordion:
        with mui.AccordionSummary:
            mui.Typography(variant="h6", children="Accordion Title")
        with mui.AccordionDetails:
            mui.Typography(children="Accordion Content")

