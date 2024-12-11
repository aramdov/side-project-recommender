import streamlit as st
from config.config_manager import get_settings
from backend.core.vector_store import VectorStore
from frontend.components.form_components import (
    render_file_upload,
    render_interest_form
)
from frontend.components.display_components import (
    render_recommendations
)

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

def main():
    # Initialize settings
    settings = get_settings()
    
    # Configure page
    st.set_page_config(
        page_title="Project Recommender",
        page_icon="🚀",
        layout="wide" if not settings.is_development() else "centered"
    )

    # Initialize session state
    initialize_session_state()

    # Page header
    st.title("🌟 Find Your Next Coding Project")
    st.write("""
    Welcome! Let's help you discover the perfect side project that aligns with 
    your skills and interests while pushing your boundaries just the right amount.
    """)

    # Initialize services (vector store, etc.)
    vector_store = VectorStore(
        api_key=settings.pinecone_api_key,
        environment=settings.pinecone_environment
    )

    # Render form components
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = render_file_upload()
            interests, experience, exploration_type = render_interest_form()
        
        with col2:
            st.info("""
            💡 **Tip**: Be specific about your interests! 
            Instead of just "web development", try "I'm interested in building 
            accessible web applications with modern frameworks like React"
            """)

    # Process form submission
    if st.button("Get Recommendations 🚀"):
        with st.spinner("Analyzing your profile..."):
            # Process inputs and generate recommendations
            # Store results in session state
            pass

    # Display recommendations if they exist
    if st.session_state.recommendations:
        render_recommendations(st.session_state.recommendations)

    # Debug information in development
    if settings.debug:
        with st.expander("Debug Information"):
            st.write("Settings:", settings.dict())
            st.write("Session State:", st.session_state)

if __name__ == "__main__":
    main()