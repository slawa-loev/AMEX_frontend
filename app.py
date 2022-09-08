from asyncore import read
import streamlit as st
from PIL import Image
from pandas import read_csv
import requests
import json



#col1, col2, col3, col4, col5 = st.columns(5)

st.set_page_config(page_title="AMEX Oracle", page_icon='',layout="wide")

amexblue = 'color: #006fcf;'
font1 = 'font-family: Helvetica;'
font2 = 'font-family: sans-serif;'
font3 = 'font-family: Helvetica-Neue;'
font4 = 'font-family: BentoSans;'
font5 = 'font-family: Garamond;'
amexlogofont = 'font-family: Handel Gothic D Bold;'
cust_font = open("style.css").read()

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    #st.markdown('AMEX ORACLE')


col2, col4 = st.columns([8, 8])
#col1, col2, col3, col4 = st.columns([1, 6, 1, 8])





amex_logo = Image.open('team_imgs/amex_oracle_logo.jpg')
col2.image(amex_logo,
           use_column_width=True,
           #width=350,
           #output_format='PNG'
           )
    # with open('template_csv/AMEX_user_template.csv') as f:
    #     if st.download_button('Example template', f, 'example_template.csv'):
    #         st.write('Thanks for downloading!')




col4.markdown(f"<h4 style='text-align: center;{font5} {amexblue}'>Will your credit card customer pay you back?</h1>", unsafe_allow_html=True)




col4.markdown(f"<h5 style='text-align: center;{font2} color: #334251;'>Dear American Express managment, </h4>", unsafe_allow_html=True)
col4.markdown(f"<h6 style='text-align: center;{font2} color: #334251;'>Please upload a CSV file in the following format: </h5>", unsafe_allow_html=True)



with open('template_csv/AMEX_client_template.csv') as f:
    if col4.download_button('Example template', f, 'example_template.csv'):
        col4.write('Thanks for downloading!')

# with open('template_csv/Slawa_Loev.csv') as s:
#     if col4.download_button('Slawa_new_customer', s, 'Slawa_Loev.csv'):
#         col4.write('Thanks for downloading!')

# with open('template_csv/Sjoerd_de_Wit.csv') as w:
#     if col4.download_button('Sjoerd_new_customer', w, 'Sjoerd_de_Wit.csv'):
#         col4.write('Thanks for downloading!')



#st.write('\n\n-------------')



with col4.form("my_form"):

    uploaded_csv_file = st.file_uploader("Upload a customer CSV File",
                                         type=['csv'],
                                        # accept_multiple_files=True
                                         )

    submitted = st.form_submit_button("Get prediction!")

default_shap = Image.open('team_imgs/sjoerd_shap_default.png')
pay_shap = Image.open('team_imgs/slawa_shap_payer.png')


if submitted:

    url_api = 'https://amex-api-results.herokuapp.com/predict'
    if uploaded_csv_file == None:
        st.markdown(f"<h1 style='text-align: center; color: {amexblue};'> </h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: {amexblue};'> </h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: red;'>Wrong submission, please upload CSV file in the right format</h5>", unsafe_allow_html=True)

    else:

        data = read_csv(uploaded_csv_file, index_col=0).fillna('').to_dict(orient='records')[0]
        params_user = {"data": json.dumps(data)}

        predictions = requests.get(url_api,
                                    params = params_user).json()

        st.write('-------------')
        st.markdown("<h4 style='text-align: center; color: black;'>Thank you for submitting</h4>", unsafe_allow_html=True)
        st.write('-------------')
        st.markdown("<h5 style='text-align: center; color: black;'>Potential customer:</h5>", unsafe_allow_html=True)

        if predictions['output'] == 'defaulter':

            html_str_custID = f"<h3 style='text-align: center; color: grey;'>{uploaded_csv_file.name[:-4].replace('_',' ')}</h3>"
            st.markdown(html_str_custID, unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center; color: black;'>will ... </h5>", unsafe_allow_html=True)
            html_str_output = f"<h2 style='text-align: center; color: red;'>not pay you back</h2>"
            st.markdown(html_str_output, unsafe_allow_html=True)
            st.markdown("<h10 style='text-align: center; color: black;'> </h10>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center; color: black;'>With probability of:</h5>", unsafe_allow_html=True)
            html_str_proba = f"<h1 style='text-align: center; color: red;'>{float(predictions['probability'])*100} %</h1>"
            st.markdown(html_str_proba, unsafe_allow_html=True)
            col1,col2,col3 = st.columns([1,3,1])
            col2.write('-------------')
            col2.image(default_shap, use_column_width=True)
            col2.write('-------------')

        else:

            html_str_custID = f"<h3 style='text-align: center; color: grey;'>{uploaded_csv_file.name[:-4].replace('_',' ')}</h3>"
            st.markdown(html_str_custID, unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center; color: black;'>will ... </h5>", unsafe_allow_html=True)
            html_str_output = f"<h2 style='text-align: center; color: green;'>pay you back</h2>"
            st.markdown(html_str_output, unsafe_allow_html=True)
            st.markdown("<h10 style='text-align: center; color: black;'> </h10>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center; color: black;'>With probability of:</h5>", unsafe_allow_html=True)
            html_str_proba = f"<h1 style='text-align: center; color: green;'>{float(predictions['probability'])*100} %</h1>"
            st.markdown(html_str_proba, unsafe_allow_html=True)
            col1,col2,col3 = st.columns([1,3,1])
            col2.write('-------------')
            col2.image(pay_shap, use_column_width=True)
            col2.write('-------------')


col1,col2,col3 = st.columns([1,1,1])
col2.markdown(f"<h1 style='text-align: center; color: {amexblue};'> </h1>", unsafe_allow_html=True)
col2.markdown(f"<h1 style='text-align: center; color: {amexblue};'> </h1>", unsafe_allow_html=True)


col2.markdown(f"<h6 style='text-align: center; color: {amexblue};'>Powered by</h6>", unsafe_allow_html=True)



team_img = Image.open('team_imgs/team.jpg')
# slawa_img = Image.open('team_imgs/slawa.jpeg')
# yuzhe_img = Image.open('team_imgs/yuzhe.jpeg')
# sjoerd_img = Image.open('team_imgs/sjoerd.jpeg')
# lewagon_img = Image.open('team_imgs/lewagon.png')




col2.image(team_img, caption="", use_column_width=True)


## CUSTOM FONT EXPERIMENTS
# css = open( "style.css" )
# st.markdown( f'<style>{css.read()} hello </style>' , unsafe_allow_html= True)



# st.markdown(""" <style> .font {
# font-size:50px ; font-family: 'Bento Sans'; color: #FF9633;}
# </style> """, unsafe_allow_html=True)
# st.markdown('<p class="font">Guess the object Names</p>', unsafe_allow_html=True)

# st.markdown(
#         """
#         <style>
# @font-face {
#   font-family: 'sff';
#   font-style: normal;
#   font-weight: 400;
#   src: url('sffb.ttf');
# }

#     html, body, [class*="css"]  {
#     font-family: 'sff';
#     font-size: 48px;
#     }
#     </style>

#     """,
#         unsafe_allow_html=True,
#     )
# st.markdown("hello")
