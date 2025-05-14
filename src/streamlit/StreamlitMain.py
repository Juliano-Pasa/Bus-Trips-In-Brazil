from buspkg import TextFunctions as tf
from buspkg import ProjectConstants

import streamlit as st

titlePlaceholder = st.empty()

st.write("""
    ANTT holds lots of data about bus trips in Brazil, from ticket prices to private or regular trips.
    I decided to take a look at this data as a personal project to practice data science,
    and fortunately I've been learning so much more.
""")

titlePlaceholder.write_stream(tf.GetCharacterStream("# Bus Trips in Brazil 🇧🇷", 0.0625))