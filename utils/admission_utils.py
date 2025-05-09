import streamlit as st
import pandas as pd


class admision():
    """
    Class for admission utils
    """

    def __init__(self):
        ...

    def file_uploader(self):
        uploaded_file = st.file_uploader("")
        return uploaded_file

    # Create a list of columns of csv files and return rhe list and its dataframe
    def create_list_frame(self, uploaded_file):
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            for _ in dataframe.columns:
                data = dataframe.columns.tolist()
            return data, dataframe

    # Checkbox container for admission
    def checkbox_container(self, data, target):
        for i, option in enumerate(data):
            if i % 5 == 0:
                # Create a new row every 5 checkboxes
                row = st.columns(5)
            with row[i % 5]:
                if option == target.name:
                    continue
                # Create the checkbox
                st.checkbox(option, key='dynamic_checkbox_' + option)
     # Get selected Checkbox
    

    def get_selected_checkboxes(self):
        return [i.replace('dynamic_checkbox_', '') for i in st.session_state.keys()
                if i.startswith('dynamic_checkbox_') and st.session_state[i]]

    def radiobox_contanier(self, data):
        selected = st.radio(options=data, label="")
        return selected
