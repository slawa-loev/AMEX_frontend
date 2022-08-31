from asyncore import read
import streamlit as st
from PIL import Image
from pandas import read_csv
import requests

# json_url = ''
# requests.get(json_url, )

api_json_data = {'customer_ID': 'abc123customer',
                'output': 'defaulter',
                'probability': '99.9'}

'''
# Is your customer a Defaulter?!
'''

st.write('\n\nDear American Express managment, \n\nPlease only upload a csv file in the format as the following example template:')


with open('template_csv/AMEX_user_template.csv') as f:
    if st.download_button('Download example template CSV', f, 'example_template.csv'):
        st.write('Thanks for downloading!')


st.write('\n\n-------------')

with st.form("my_form"):

    csv_file = st.file_uploader("Upload a customer CSV File",type=['csv'], )

    submitted = st.form_submit_button("Get prediction!")

if submitted:
    st.write('-------------',
             '\n\nThank you for submitting',
             f'\n\nYour customer with customer_ID: {api_json_data["customer_ID"]} must be a {api_json_data["output"]}!!!!',
             f'\n\nWith probability of {api_json_data["probability"]} %',
             '\n\n-------------')


isis_img = Image.open('team_imgs/isis.jpeg')
slawa_img = Image.open('team_imgs/slawa.jpeg')
yuzhe_img = Image.open('team_imgs/yuzhe.jpeg')
sjoerd_img = Image.open('team_imgs/sjoerd.jpeg')
lewagon_img = Image.open('team_imgs/lewagon.png')


st.write('\n\n\n\nThis wonderful predictor is brought to you by:')


st.image([isis_img, slawa_img, yuzhe_img, sjoerd_img, lewagon_img],
         caption=['Isis!', 'Slawa!', 'Yuzhe!', 'Sjoerd!', 'Le Wagon!'], width=100)
