from asyncore import read
import streamlit as st
from PIL import Image
from pandas import read_csv
import requests
import json
from shap.shap import make_shap_plot, data_agg
import matplotlib.pyplot as plt
import joblib
import shap


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


col1, col2 = st.columns([10, 8])

amex_logo = Image.open('team_imgs/amex_oracle_logo.jpg')
col1.image(amex_logo,
           use_column_width=True,
           #width=350,
           #output_format='PNG'
           )
    # with open('template_csv/AMEX_user_template.csv') as f:
    #     if st.download_button('Example template', f, 'example_template.csv'):
    #         st.write('Thanks for downloading!')




col2.markdown(f"<h4 style='text-align: center;{font5} {amexblue}'>Will your credit card customer pay you back?</h4>", unsafe_allow_html=True)




col2.markdown(f"<h5 style='text-align: center;{font2} color: #334251;'>Dear American Express managment, </h5>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: center;{font2} color: #334251;'>Please upload a CSV file in the following format: </h6>", unsafe_allow_html=True)


with open('template_csv/template.csv') as f:
    if col2.download_button('Template', f, 'template.csv'):
        col2.write('Thanks for downloading!')



col2.markdown(f"<h6 style='text-align: left;{font2} color: #334251;'>Features should be anonymized and normalized, and fall into the following general categories: </h6>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: left;{font2} color: #334251;'>D_* = Delinquency variables </h6>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: left;{font2} color: #334251;'>S_* = Spend variables </h6>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: left;{font2} color: #334251;'>P_* = Payment variables </h6>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: left;{font2} color: #334251;'>B_* = Balance variables </h6>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: left;{font2} color: #334251;'>R_* = Risk variables </h6>", unsafe_allow_html=True)

st.write('-------------')




st.markdown(f"<h6 style='text-align: center;{font2} color: #334251;'>You can use these examples to try out the ORACLE: </h6>", unsafe_allow_html=True)


col3, col4, col5, col6 = st.columns([8, 5, 5, 8])

with open('template_csv/example_payer.csv') as f:
    col4.download_button('Data example #1', f, 'data_example_1.csv')


with open('template_csv/example_defaulter.csv') as s:
    col5.download_button('Data example #2', s, 'data_example_2.csv')


col7, col8, col9 = st.columns([1, 3, 1])


with col8.form("my_form"):

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

        data = read_csv(uploaded_csv_file, index_col=0)
        data_dict = data.fillna('').to_dict(orient='records')[0]
        params_user = {"data": json.dumps(data_dict)}

        predictions = requests.get(url_api,
                                    params = params_user).json()


        if predictions['customer_ID'] == 0:
            st.markdown("<h5 style='text-align: center; color: red;'> Template does not give output, please upload a csv with data </h5>", unsafe_allow_html=True)
        else:

            st.write('-------------')
            st.markdown("<h4 style='text-align: center; color: black;'>Thank you for submitting</h4>", unsafe_allow_html=True)
            st.write('-------------')
            st.markdown("<h5 style='text-align: center; color: black;'>Potential customer:</h5>", unsafe_allow_html=True)

            if predictions['output'] == 'defaulter':

                html_str_custID = f"<h6 style='text-align: center; color: grey;'>{predictions['customer_ID']}</h6>"
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
                #make_shap_plot(data) ## see here: https://github.com/slundberg/shap/issues/1417 for debugging
                X_pred_agg = data_agg(data).drop(columns=['customer_ID'])

                #load the explainer - sent as a separate file, to be loaded in repository
                ex_filename = 'explainer.bz2'
                ex2 = joblib.load(filename=ex_filename)

                shap_values = ex2(X_pred_agg,check_additivity=False)

                shap.plots.waterfall(shap_values[0])
                st.pyplot(bbox_inches='tight')
                plt.clf()

            else:

                html_str_custID = f"<h6 style='text-align: center; color: grey;'>{predictions['customer_ID']}</h6>"
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
                #make_shap_plot(data)
                X_pred_agg = data_agg(data).drop(columns=['customer_ID'])

                #load the explainer - sent as a separate file, to be loaded in repository
                ex_filename = 'explainer.bz2'
                ex2 = joblib.load(filename=ex_filename)

                shap_values = ex2(X_pred_agg,check_additivity=False)

                shap.plots.waterfall(shap_values[0])
                st.pyplot(bbox_inches='tight')
                plt.clf()


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
