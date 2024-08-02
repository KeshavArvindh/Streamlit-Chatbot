import streamlit as st
from gtts import gTTS
import os
import time
import base64
import re
import speech_recognition as sr
import google.generativeai as genai
from langchain_core import *
from langchain_core.messages import HumanMessage, AIMessage

genai.configure(api_key="Your-Api-key")
model = genai.GenerativeModel('gemini-1.5-flash')

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def generate_response_gemini(query):
    response = model.generate_content(query)
    T = response.text
    clean_text = re.sub(r'\*\*', '', T)
    clean_text = clean_text.replace('\n', ' ').replace('\r', '')
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text

def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        st.session_state.info_placeholder.info("Please speak now")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.error("Listening timed out while waiting for phrase to start")
        except sr.RequestError:
            st.error("API unavailable or unresponsive")
        except sr.UnknownValueError:
            st.error("Unable to recognize speech")
        return None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Streaming bot")
st.title("Streaming bot")

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

st.header("Ask a Question")

col1, col2, col3 = st.columns([0.8, 0.1, 0.2])

user_query = None
with col1:
    user_query = st.text_input("Enter your question:", key="input_box")

with col2:
    info_placeholder = st.empty()
    if st.button("🎤"):
        st.session_state.info_placeholder = info_placeholder
        speech_query = recognize_speech_from_mic()
        if speech_query:
            user_query = speech_query
        info_placeholder.empty()

with col3:
    if st.button("Enter"):
        user_query = st.session_state.input_box

if user_query:
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response_container = st.empty()
        ai_response = ""
        full_response = generate_response_gemini(user_query)
        audio_file = text_to_speech(full_response, "response.mp3")
        tokens = full_response.split()
        autoplay_audio(audio_file)
        for token in tokens:
            ai_response += token + " "
            response_container.markdown(ai_response)
            time.sleep(0.4)
        st.audio(audio_file)
        st.session_state.chat_history.append(AIMessage(ai_response.strip()))
