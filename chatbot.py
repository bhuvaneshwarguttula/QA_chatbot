#pip install -r requiremnts.txt

from dotenv import load_dotenv
load_dotenv() # loading environment variables

# from streamlit_chat import message
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#func to load genmini pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = model.generate_content(question, stream=True) #not to wait for entire response
    return response

#initiate our steamlit app
st.set_page_config(
    page_title="Your own BOT",
    page_icon="🤖"
    )

st.header("Your own BOT 🤖")

input = st.chat_input("Message BOT: ", key="input")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if input:
    st.chat_input(key="disable_input",disabled=True)
    with st.chat_message("user"):
        st.markdown(input)
    st.session_state.messages.append({"role": "user", "content": input})

    response = get_gemini_response(input)
    with st.chat_message("assistant"):
        for chunk in response:
            st.markdown(chunk.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()