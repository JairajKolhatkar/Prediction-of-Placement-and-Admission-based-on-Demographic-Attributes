import time
import extra_streamlit_components as stx
import streamlit as st
from streamlit_lottie import st_lottie_spinner
#------------------Object init------------------#
cookies = stx.CookieManager(key="logout")
#-----------------------------------------------#


def logout():
    cookies.delete(cookie="email")
    return 