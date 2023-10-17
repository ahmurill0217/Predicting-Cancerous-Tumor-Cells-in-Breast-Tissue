import streamlit as st
import pandas as pd
import scikit-learn as sklearn
from PIL import Image
import subprocess
import os
import base64
import pickle

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('Predicting_Cancerous_Tumor_Cells_in_Breast_Tissue.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='Malignant is (1) and Benign is (0)')
    df = pd.concat([prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# Logo image
image = Image.open('logo.jpg')

st.image(image, use_column_width=True)

# Page title
st.markdown("""
# Cancerous Tumor Cells Prediction App 

This app allows you to accurately predict if patient sample is malignant- a '1' denotes cancerous cells and '0' denotes a benign sample. 

**Credits**
- App built in `Python` + `Streamlit` by Angel Murillo 
---
""")

# Sidebar
with st.sidebar.header('1. Upload your TXT data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    st.sidebar.markdown(r"""
[Example input file](C: Top 9 features.txt)
""")

if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('Input_Data', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Predicting..."):
        build_model(load_data)
else:
    st.info('Upload input data in the sidebar to start!')