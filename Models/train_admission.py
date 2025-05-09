from os import path
import streamlit as st
import pandas as pd
from utils import database as db
from utils import admission_utils
from Neural_Model.model_sgd_admission import default_model_training, custom_model_training
import extra_streamlit_components as stx

# ------------------------Object initializations---------------------------------#
adutil = admission_utils.admision()
# -------------------------------------------------------------------------------#


def train_admission(user, cookie_manager):
    id = db.fetch_user_id(user)
    if path.exists(f"Main_Models\\{id}\\admission_model\\model") or path.exists(f"Main_Models\\{id}\\admission_model\\model.joblib"):
        st.warning(
            "Model already has been trained. Be cautious while re-training the model. It will overwrite existing one")
    st.header("Choose CSV file")
    uploaded_file = adutil.file_uploader()
    if uploaded_file is not None:
        data, dataframe = adutil.create_list_frame(uploaded_file)
        with st.expander("Select what you want to predict"):
            inputData = []
            for i in dataframe:
                if len(pd.value_counts(dataframe[i])) == 2:
                    inputData.append(i)
            target = dataframe[adutil.radiobox_contanier(inputData)]

        with st.expander("Select features on basis of which you want to buld model"):
            st.header('Select the type of features')
            c1 = st.radio('', ('Custom features', 'Default features'))
            if c1 == 'Custom features':
                try:
                    st.header('Select features\n')
                    adutil.checkbox_container(data, target)
                    c = adutil.get_selected_checkboxes()
                    features = dataframe[c]
                    db.add_admission_features_to_database(user, c)
                except TypeError or NameError as err:
                    st.write(err)
                    st.write("Please Select CSV File")
            if c1 == 'Default features':
                st.subheader(':green[Be relax]')
                st.info(
                    "All the features selection and model training will be done automatically. Please Go to 'Train the model' below and start the training by clicking on button")

        # -----------------Train the model---------------------------------#
        with st.expander("Train the model"):
            if c1 == "Custom features":
                if st.button("Train the Model"):
                    custom_model_training(
                        features, target, dataframe, st, cookie_manager)
            if c1 == "Default features":
                if st.button("Train the Model"):
                    default_model_training(
                        dataframe, target, data, st, cookie_manager)
    else:
        st.header("Please Select CSV file")
