import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

with st.sidebar:
    st.markdown("# Announcements")
    st.markdown(
        """              
    Keep an eye in this section for latest news and announcements.     
                """
    )

st.markdown(
    f'<h1 style="color:#202a44; font-size:42px; "> Welcome to EMPATHY Coach! </h1>',
    unsafe_allow_html=True,
)

st.markdown(
    """
EMPATHY Coach is a feedback web application developed by [Srihari Sridhar](https://mays.tamu.edu/directory/shrihari-sridhar/) and [Pallav Routh](https://uwm.edu/business/people/routh-pallav/).
    
The app is designed to support reviewers of academic articles by streamlining the peer review process. Using an advanced feedback framework called E.M.P.A.T.H.Y., the app helps reviewers provide constructive, actionable, and high-quality feedback to authors.

Simply upload your article review document, and the app leverages a cutting-edge language model (LLM) to analyze your review, identify areas for enhancement, and offer targeted suggestions. 

The app enables users to review, accept, or reject suggestions, apply changes seamlessly, and generate an updated review document—all in one intuitive interface. Once finalized, the improved review document can be downloaded.
"""
)

st.markdown("---")

st.markdown(
    f'<h1 style="color:#202a44; font-size:42px; "> Disclaimer ‼️ </h1>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    Text here.
    """
)
