from buspkg import TextFunctions as tf
from buspkg import ProjectConstants

import streamlit as st

st.write_stream(tf.GetCharacterStream("# Bus Trips in Brazil!", 0.0625))