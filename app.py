from http.client import responses
from logging import exception

import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ You are a Youtube Video summarizer. You will be taking the Transcript text and summarising the entire video and providing the important summary in points within 250 to 300 Words. Please Provide of the summary of the text given here :"""

transcript_text = None

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " "
        for i in transcript_text:
            transcript += " " + i["text"]
            return transcript

    except Exception as e:
        raise e


def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response =model.generate_content(prompt + transcript_text)
    return response.text


#Creating Streamlit app

st.title("YOUTUBE TRANSCRIPT TO DETAIL DESCRIPTION CONVERTER")
youtube_link = st.text_input("Enter Youtube Video Link Here:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

if transcript_text:
    summary = generate_gemini_content(transcript_text,prompt)
    st.markdown("## Detailed_Notes:")
    st.write(summary)




