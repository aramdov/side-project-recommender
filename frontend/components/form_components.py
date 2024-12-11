import streamlit as st
from typing import Tuple

def render_file_upload() -> str:
    """Render the file upload component"""
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)", 
        type="pdf",
        help="Your resume helps us understand your current skill level"
    )
    return uploaded_file

def render_interest_form() -> Tuple[str, str, str]:
    """Render the interests and experience form"""
    interests = st.text_area(
        "What are your interests and passions in tech?",
        placeholder="E.g., I'm fascinated by AI and machine learning, especially natural language processing...",
        help="Be specific about what excites you!"
    )
    
    experience = st.text_area(
        "Describe your relevant experience",
        placeholder="E.g., I've built a few small web apps using React and Node.js...",
        help="Include both academic and personal projects"
    )
    
    exploration_type = st.select_slider(
        "How far do you want to venture from your comfort zone?",
        options=[
            "Stay in my comfort zone",
            "Slightly challenging",
            "Push my boundaries",
            "Explore new territory"
        ],
        value="Slightly challenging",
        help="This helps us calibrate the difficulty of project suggestions"
    )
    
    return interests, experience, exploration_type