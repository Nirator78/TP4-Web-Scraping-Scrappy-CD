# Display allocine.csv in stremlit

import streamlit as st
import pandas as pd

dfAllocine = pd.read_csv('allocine.csv')
st.write(dfAllocine)

dfBoursorama = pd.read_csv('boursorama.csv')
st.write(dfBoursorama)