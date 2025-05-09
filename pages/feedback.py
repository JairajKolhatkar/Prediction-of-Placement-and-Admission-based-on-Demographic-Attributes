import time
import openai
import pandas as pd
from Neural_Model.model_sgd_admission import load_lottiefile
import streamlit as st
from utils.database import remove_user, fetch_user_id, AddFeedbacK, FetchFeedback
import extra_streamlit_components as stx
from utils import redirect as rd
from streamlit_lottie import st_lottie
from utils import logout
import extra_streamlit_components as stx


#--------------------------Obj initialization---------------#
cookkies = stx.CookieManager()
user = cookkies.get(cookie='email')  # GEtting user from cookie
#-----------------------------------------------------------#

#--------------------Loading custom css---------------#

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("css\\admission_css.css")
#---------------------------------------------------#

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


#--------------------------Feedback start from here---------------------#


def generate_autoresponse(review_text, reviewer_name):
    # Use environment variable for API key instead of hardcoding
    openai.api_key = "YOUR_API_KEY_HERE" # Replace with environment variable in production
    prompt = f'Autoresponse to review : \n\n{review_text} from user who has name as \n\n{reviewer_name}\n\n also include best regards from team name AAP team'

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    return response.choices[0].text.strip()


if user:
    st.header("Please submit your review")
    reviewer_name = st.text_input("Enter Your name")
    review_text = st.text_area("Enter a review:")
    if st.button("Submit"):
        autoresponse = generate_autoresponse(review_text, reviewer_name)
        st.subheader(autoresponse)
        AddFeedbacK(reviewer_name, review_text)

    result=FetchFeedback()
    df=pd.DataFrame(result,columns=['Id','Name of reviewer','Review'])
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none; text-align:center}
            tbody td {text-align: center}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(df)
    