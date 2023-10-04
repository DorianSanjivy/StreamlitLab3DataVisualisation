# streamlit run second_app.py

import streamlit as st
import pandas as pd
import numpy as np

st.write('Hello, *World!* :sunglasses:')

st.write(1234)
st.write(pd.DataFrame({
          'first column': [1, 2, 3, 4],
          'second column': [10, 20, 30, 40],
}))

st.metric(label="Précision", value="95%", delta="2%")

data_json = {
    "nom": "Dupont",
    "prénom": "Jean",
    "âge": 30,
    "adresse": {
        "rue": "Rue de Paris",
        "code postal": "75001",
        "ville": "Paris"
    }
}

st.json(data_json)

