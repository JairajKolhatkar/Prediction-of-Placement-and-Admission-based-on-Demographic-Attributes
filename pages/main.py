import streamlit as st
from streamlit_option_menu import option_menu
from utils import redirect as rd

#--------------------Loading custom css---------------#


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("css\\styles.css")
#---------------------------------------------------#


#-----------------------Objects initializations----------------#

#--------------------------------------------------------------#


def main():
    #-------------------- Default Sidebar------------------------#
    with st.sidebar:
        selected = option_menu(
            menu_title="Welcome to Aadmission & Placement prediction",
            options=['Admission Prediction', 'Placement Prediction'],
            icons=["lock", "door-open"],
            orientation='vertical',
            default_index=0
        )
    #-------------------------------------------------#
    if selected == "Admission Prediction":
        rd.switch_page('admission')
    else:
        rd.switch_page('placement')


main()
