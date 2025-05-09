import datetime
import json
import re
from os.path import exists
import time
from streamlit_option_menu import option_menu
from utils import database
from utils import Krypto as kr
from utils import redirect as rd
import streamlit as st
import extra_streamlit_components as stx
from streamlit_lottie import st_lottie

#--------------------App settings -------------------#
title = "Admission and Placement Prediction"
icon = ":mag_right:"
layout = "wide"
initial_sidebar_state = "collapsed"
#----------------------------------------------------#
st.set_page_config(page_title=title, page_icon=icon,
                   layout=layout, initial_sidebar_state=initial_sidebar_state)

#--------------------Loading custom css---------------#


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("css\\styles.css")
#---------------------------------------------------#

#-------------------Lottie animation reading----------------#


def load_lottiefile(filepath: str):
    with open(filepath, "rb") as f:
        return json.load(f)
#---------------------------------------------------#


#------------------Object initializations--------------------#

db = database.CRUD()  # Database object
cookie_manager = stx.CookieManager()  # Cookie manager

#------------------------------------------------------------#


#-------------------- Default Sidebar------------------------#
with st.sidebar:
    selected = option_menu(
        menu_title="Welcome to APP",
        options=['Sign up', 'Login'],
        icons=["lock", "door-open"],
        orientation='horizontal',
        default_index=0
    )

    st_lottie(load_lottiefile(
        "assests\\lottianimations\\welcome.json"), key="welcome lottifile", height=400, width="auto", speed=5)
#-------------------------------------------------#


#--------------Email validation regex--------------#
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check(email):
    if(re.search(regex, email)):
        return True
    else:
        return False
#-------------------------------------------------#


#---------------------Checking for the cookies first---------------------#
user = cookie_manager.get(cookie="email")


if user is None:
    #------------------------Sign up and login functionality-----------------------#
    if selected == 'Sign up':

        st.header("Welcome :wave: Create your account for free", anchor="signup")
        with st.form("signup"):
            # Add form fields using the st.text_input() and st.text_area() functions
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input(
                "Confirm Password", type="password")

            # Add a form submit button using the st.form_submit_button() function
            submitted = st.form_submit_button("Sign Up")

            # Check if the form has been submitted
            if submitted:
                # Validate the form data
                if email.strip() == " " and password.strip() == " " and confirm_password.strip() == " ":
                    st.error("Fillout all the fields in the form")
                elif not check(email):
                    st.error("Invalid email")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    if db.check_user_for_signup(email):
                        st.error("User already exist! Please login")
                    else:
                        # Saving user to database
                        db.insert_user(email, password)
                        st.balloons()
                        st.success(
                            "You have successfully signed up! Click on login button now.")
    elif selected == 'Login':
        st.header("Welcome Back :smile:, Enter credentials to Login",
                  anchor="signin")
        with st.form("sign in"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            # Add a form submit button using the st.form_submit_button() function
            submitted = st.form_submit_button("Login")

            # Check if the form has been submitted
            if submitted:
                # Validate the form data
                if email.strip() == " " and password.strip() == " ":
                    st.error("Fillout all the fields in the form")
                elif not check(email):
                    st.error("Invalid Email")
                else:
                    # Save the form data to a database or perform other actions
                    if(db.check_user_for_login(email, password)):
                        cookie_manager.set("email", kr.hash_generator(
                            email), expires_at=datetime.datetime.now() + datetime.timedelta(hours=1))
                        st.success("Redirecting!")
                        time.sleep(2)
                        st.experimental_rerun()
                    else:
                        st.error("User does not exist!")
elif user is not None:
    rd.switch_page("main")

