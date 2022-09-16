import streamlit as st
from PIL import Image
from pandas import read_csv
import requests
import json
from shap_folder.shap_script import make_shap_plot
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)


# from catboost import *



st.set_page_config(page_title="AMEX ORACLE", page_icon='',layout="wide")

amexblue = 'color: #006fcf;'

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




col2.markdown(f"<h4 style='text-align: center; {amexblue}'>Will your credit card customer pay you back?</h4>", unsafe_allow_html=True)




col2.markdown(f"<h5 style='text-align: center; color: #334251;'>Dear American Express managment, </h5>", unsafe_allow_html=True)
col2.markdown(f"<h6 style='text-align: center; color: #334251;'>Please upload a CSV file in the following format: </h6>", unsafe_allow_html=True)


with open('template_csv/template.csv') as f:
    if col2.download_button('Template', f, 'template.csv'):
        col2.write('Thanks for downloading!')



col2.markdown(f"<h6 style='text-align: left; color: #334251;'>Features should be anonymized and normalized, and fall into the following general categories: </h6>", unsafe_allow_html=True)
col2.markdown(f"<h7 style='text-align: left; color: #334251;'>D_* = __Delinquency variables__ have to do with the customer being late in paying their debt. </h6>", unsafe_allow_html=True)

col2.markdown(f"<h7 style='text-align: left; color: #334251;'>S_* = __Spend variables__ have to do with the customer's spending behavior. </h6>", unsafe_allow_html=True)

col2.markdown(f"<h7 style='text-align: left; color: #334251;'>P_* = __Payment variables__ have to do with the customer's behavior when paying back debt. </h6>", unsafe_allow_html=True)

col2.markdown(f"<h7 style='text-align: left; color: #334251;'>B_* = __Balance variables__ have to do with the customer's account balance. </h6>", unsafe_allow_html=True)

col2.markdown(f"<h7 style='text-align: left; color: #334251;'>R_* = __Risk variables__ have to do with other factors that increase the default risk of a customer. </h6>", unsafe_allow_html=True)


st.write('-------------')




st.markdown(f"<h6 style='text-align: center; color: #334251;'>You can use these examples to try out the ORACLE: </h6>", unsafe_allow_html=True)


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
                col1,col2,col3 = st.columns([1,5,1])
                col2.write('-------------')


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
                col1,col2,col3 = st.columns([1,5,1])
                col2.write('-------------')

            col2.write("""
                       Below is a graph visualizing the impact of various pieces of information about
                       the customer (features) on the ORACLE's prediction.
                       The 10 most important features are seperately displayed.
                       Features with D, S, P, B, R relate to
                       delinquency, spending, payment, balance and risk variables respectively (see above).
                       The bigger a bar,
                       the more influence a feature had on the ORACLE's prediction. If a bar is red,
                       then this feature speaks in favor of the customer not paying back.
                       If a feature is blue, then this feature speaks in favor of a customer paying back.
                       """)
            shap_graph, shap_values = make_shap_plot(data)
            col2.pyplot(shap_graph, bbox_inches='tight')
            plt.clf()
            #col2.write("Here is a graph visualizing the impact various pieces of information about the customer (features) had on the ORACLE's prediction.")
            col2.write('-------------')

col1,col2,col3 = st.columns([1,1,1])
col2.markdown(f"<h1 style='text-align: center; color: {amexblue};'> </h1>", unsafe_allow_html=True)
col2.markdown(f"<h1 style='text-align: center; color: {amexblue};'> </h1>", unsafe_allow_html=True)


col2.markdown(f"<h6 style='text-align: center; color: {amexblue};'>Powered by</h6>", unsafe_allow_html=True)



team_img = Image.open('team_imgs/team.jpg')


col2.image(team_img, caption="", use_column_width=True)
