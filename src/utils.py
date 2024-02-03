import streamlit as st
from streamlit_extras.app_logo import add_logo

def page_configuration(title: str):
    """
    Sets the configuration for the page and adds a logo and title

    Arguments:
        title (str): the title of the page
    """
    # Set the page configuration
    st.set_page_config(
        page_title=title,
        page_icon='assets/images/logo.svg',
        layout='wide',
        initial_sidebar_state="expanded"
    )

    # Add the logo for the application
    add_logo('assets/images/logo-100.png', height=80)

    # Add the title for the page
    st.title(title)