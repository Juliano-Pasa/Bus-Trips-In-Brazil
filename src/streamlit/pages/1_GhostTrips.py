from buspkg import TextFunctions as tf
from buspkg import ProjectConstants

import streamlit as st

titlePlaceholder = st.empty()

st.write("""
         ANTT holds records of regular trips registered from 2019 to 2024. 
         However, some of the trips are duplicates or wrongly inserted records. 
         Because of this, there are several "trips" of the same bus departing at the same time, 
         which I decided to name as **ghost trips**.
""")

titlePlaceholder.write_stream(tf.GetCharacterStream("# Ghost Trips 👻"))