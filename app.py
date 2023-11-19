import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import pandas as pd
import sklearn
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import subprocess
import os
import base64
import pickle

# --- USER AUTHENTICATION ---
names = ["IT Associate", "Registered Nurse", "Physician"]
usernames = ["IT", "rnurse", "physician"]

#----Load hashed passwords----
file_path = Path(r'C:\Users\Admin\Desktop\Capstone Project\generate_keys.py').parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(
    names=names,
    usernames=usernames,
    passwords=hashed_passwords,
    cookie_name="Tumor_Cell_Prediction",
    key="abcdef",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

#----File download----
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
        return href

    #----Model building----
    def build_model(dataframe):
        # Reads in saved regression model
        load_model = pickle.load(open('Predicting_Cancerous_Tumor_Cells_in_Breast_Tissue.pkl', 'rb'))
        # Apply model to make predictions
        prediction = load_model.predict(dataframe)
        st.header('**Prediction output**')
        prediction_output = pd.Series(prediction, name='Malignant (1) or Benign (0)')
        df = pd.concat([prediction_output], axis=1)
        st.write(df)
        st.markdown(filedownload(df), unsafe_allow_html=True)
        st.markdown(""" 
        # Prediction Note
        The task specific model for this data product is a **random forest** model with a **97% plus accuracy**, it was trained on the Wisconsin Breast
        Cancer Dataset which is considered the gold standard for breast cancer prediction. An out value of "1" indicates a malignant sample exemplifying cancerous characteristics and a "0" inidicated a benign sample. 
        Please use predicted outcomes as a secondary measure when observing Fine Needle Aspirate test results  """)

    #----Interactive Plot----
    def interactive_plot(dataframe):
        # Create a radio button for plot selection
        plot_type = st.radio('Choose a plot type:', ('Scatter Plot', 'Correlation Heatmap'))

        if plot_type == 'Scatter Plot':
            col1, col2 = st.columns(2)

            x_axis_val = col1.selectbox('Select the X-axis', options=dataframe.columns)
            y_axis_val = col2.selectbox('Select the Y-axis', options=dataframe.columns)

            plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val)
            st.plotly_chart(plot, use_container_width=True)

        elif plot_type == 'Correlation Heatmap':
            corr = dataframe.corr()
            heatmap = go.Figure(go.Heatmap(
            z=corr.values, 
            x=corr.columns, 
            y=corr.columns, 
            colorscale='RdBu',
            zmin=-1,
            zmax=1
        ))
            for i in range(len(corr.columns)):
                for j in range(len(corr.columns)):
                    heatmap.add_annotation(go.layout.Annotation(
                        text=str(round(corr.iloc[i, j], 2)),
                        x=corr.columns[j],
                        y=corr.columns[i],
                        showarrow=False,
                        font=dict(color='black' if -0.5 < corr.iloc[i, j] < 0.5 else 'white')
                    ))

            st.plotly_chart(heatmap, use_container_width=True)



    #----Data statistics----
    def data_summary(dataframe):
        st.header('Statistics of Dataframe')
        st.write(dataframe.describe())
        st.markdown(""" This dataframe is a quick summary of the central tendencies, dispersion, and shape of a dataset's distribution.  """)


    #----Sidebar----
    authenticator.logout("Logout", "sidebar")
    with st.sidebar.header('1. Upload your data'):
        upload_file = st.sidebar.file_uploader("Upload your input file", type=['csv'])
    #Sidebar navigation
    options = st.sidebar.radio('Select what you want to display:', ['Home', 'Data Summary', 'Data Plots', 'Analysis'])

    # Check if file has been uploaded
    if upload_file is not None:
        df = pd.read_csv(upload_file)

    # Navigation options   
    if options == 'Home':
        image = Image.open('logo.jpg')
        st.image(image, use_column_width=True)
        st.markdown("""
        # Cancerous Tumor Cell Prediction 
        Each year in the United States, about 240,000 cases of breast cancer are diagnosed in women and about 2,100 in men.This app allows you to accurately predict if a patient sample is cancerous. By inputing the 
        9 Fine Needle Aspirate features recommended in the user guide and training, the data product will be able to accurately predict the patient's results, a **'1'** signifies a cancerous sample and a **'0'** denotes a benign sample.
    
        **Credits**
        - App built in `Python` + `Streamlit` by Angel Murillo 
        ---
        """)
        st.info('Upload input data in the sidebar to start!')   
    elif options == 'Data Summary':
        data_summary(df)
    elif options == 'Data Plots':
        interactive_plot(df)
    elif options == 'Analysis':
        build_model(df)
