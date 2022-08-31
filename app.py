import streamlit as st
import datetime
import requests


'''
# Is your customer a Defaulter?!
'''

with st.form("my_form"):

    csv_file = st.file_uploader("Upload a customer CSV File",type=['csv'])

    submitted = st.form_submit_button("Get prediction!")

if submitted:
    st.write('-------------',
             '\n\nThank you for submitting',
             '\n\nYour customer must be a defaulter!!!!',
             '\n\nWith probability of 99.9 %',
             '\n\n-------------')
