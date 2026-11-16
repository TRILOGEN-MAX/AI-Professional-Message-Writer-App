"""
BlackHole AI - Professional Message Writer Web Application.
Main entry point and orchestrator.
"""

import streamlit as st
import os

# 1. Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="BlackHole AI - Professional Message Writer",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Black Hole Deep Space Styling
def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "background.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

# 3. Import UI components and view modules
from components.sidebar import render_sidebar
from views.home import render_home_page
from views.generator import render_generator_page
from views.history import render_history_page
from views.settings import render_settings_page
from views.about import render_about_page

# 4. Initialize Session State for robust navigation and configuration
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if "setting_default_platform" not in st.session_state:
    st.session_state["setting_default_platform"] = "Email"

if "setting_default_tone" not in st.session_state:
    st.session_state["setting_default_tone"] = "Professional"

# 5. Render Sidebar Navigation
render_sidebar()

# 6. Route to the active page
current_page = st.session_state.get("current_page", "Home")

if current_page == "Home":
    render_home_page()
elif current_page == "Create Message":
    render_generator_page()
elif current_page == "Message History":
    render_history_page()
elif current_page == "Settings":
    render_settings_page()
elif current_page == "About":
    render_about_page()
else:
    st.session_state["current_page"] = "Home"
    render_home_page()
