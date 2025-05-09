import time
from Models.train_admission import train_admission
from Models.use_admission import use_admission
from Neural_Model.model_sgd_admission import load_lottiefile
import streamlit as st
from utils.database import remove_user, fetch_user_id
import extra_streamlit_components as stx
from utils import redirect as rd
from utils import logout
from streamlit_lottie import st_lottie
#------------------Object initializations--------------------#
cookie_manager = stx.CookieManager(key="adnissionpage")  # Cookie manager

#------------------------------------------------------------#

#------------------------------Important variables-------------------------#
user = cookie_manager.get(cookie="email")
#-------------------------------------------------------------------------#


#--------------------Loading custom css---------------#


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("css\\admission_css.css")
#---------------------------------------------------#


#--------------------Main App------------------------#


#-------------------- Default Sidebar------------------------#
with st.sidebar:
    placement = st.button("Switch to Placement Page")
    admission = st.button("Switch to Admission Page")
    logout_button = st.button("Logout")
    delete_account = st.button("Delete Acoount")
    give_feedback = st.button("Give Feedback")
    if placement:
        rd.switch_page('placement')
    if admission:
        rd.switch_page('admission')

#-------------------------------------------------#

#-------------------Logout button-----------------#
try:
    if logout_button:
        st.snow()
        time.sleep(3)
        logout.logout()
except:
    st.error("You are already logged out!!")

#------------------Delete account button-----------#

if delete_account:
    try:
        st_lottie(load_lottiefile("assests\lottianimations\delete.json"),
                  height=500, width='100%')
        id = fetch_user_id(user)
        remove_user(user, id)
        time.sleep(2)
        logout.logout()
    except TypeError as err:
        st.error("Your account has already been deleted")
#--------------------------------------------------#

#------------------------------------FeedBack button--------------------#
if give_feedback:
    if user:
        rd.switch_page("feedback")
#------------------------------------------------------------------------#


#---------------------Checking for the cookies first---------------------#
time.sleep(1)
if user is None:
    st.error(
        "User not logged in! [Login Again](http://localhost:8501/)")  # Change this link from server
else:
    st.header("Admisison Page")
    tab1, tab2 = st.tabs(["Train Model", "Use model"])
    with tab1:
        train_admission(user, cookie_manager)
    with tab2:
        use_admission(user)
