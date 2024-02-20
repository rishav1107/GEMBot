from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response.resolve()
    return ' '.join([chunk.text for chunk in response])

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
st.set_page_config(
    page_title="GeMBot",
    page_icon=":robot_face:",
    layout="wide"
)

st.title(":speech_balloon: GeMBot")

input_text = st.text_input("You:", key="input")

submit_button = st.button("Ask the Question :rocket:")

if submit_button and input_text:
    response = get_gemini_response(input_text)

    st.session_state['chat_history'].append(("You", input_text))
    
    st.subheader(":robot_face: Bot:")
    st.write(response)
    st.session_state['chat_history'].append(("Bot", response))

st.subheader(":scroll: Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}:", text)
