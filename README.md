Streaming Bot
Overview
This project is a Streamlit-based chatbot application that uses Google's Gemini Generative Model to generate responses. The application can take user inputs via text or speech, process them, and provide responses both in text and audio formats. The audio response is generated using Google's Text-to-Speech (gTTS) library. The application also supports real-time streaming of the AI's response token by token.

Features
Text Input: Users can type their questions in the input box.
Speech Input: Users can use their microphone to ask questions.
Real-Time Streaming: The AI's response is displayed token by token, providing a dynamic interaction.
Audio Response: The response is converted to speech and played back automatically.
Chat History: The conversation history is maintained throughout the session.
Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.7+
Streamlit
gTTS
SpeechRecognition
pyaudio
google-generativeai
langchain-core

Installation
Clone the repository:
git clone https://github.com/yourusername/streaming-bot.git
cd streaming-bot

Install the required Python packages:
pip install streamlit gtts SpeechRecognition pyaudio google-generativeai langchain-core
Set up your Google Generative Model API key:
Replace "AIzaSyCkFfYYLmmR9BGVlBrPVvfEAWJQ6a4ORzI" with your actual API key in the code.

Usage
Run the Streamlit app:
streamlit run app.py
Open your web browser and navigate to the URL provided by Streamlit (typically http://localhost:8501).
Interact with the bot by typing in the input box or using the microphone button to speak your query.

Code Explanation

1)Imports and Configuration
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
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

2)Helper Functions
autoplay_audio(file_path: str): Converts the audio file to base64 and embeds it into an HTML audio tag for autoplay.
generate_response_gemini(query): Generates a response using the Gemini model and cleans the text.
text_to_speech(text, filename="response.mp3"): Converts text to speech using gTTS and saves it as an MP3 file.
recognize_speech_from_mic(): Captures audio from the microphone and converts it to text using Google's Speech Recognition API.

3)Streamlit UI and Logic
Initializes the chat history and sets up the Streamlit page configuration.
Displays the chat history.
Provides input methods for text and speech.
Processes the user query and generates an AI response.
Streams the AI's response token by token and plays the audio.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Streamlit
gTTS
SpeechRecognition
Google Generative AI
Langchain Core
Contact
If you have any questions or feedback, please feel free to reach out at akeshav0601@gmail.com.

This README file provides a comprehensive overview of the project, including installation instructions, usage guidelines, and a brief explanation of the code.
