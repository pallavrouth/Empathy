import streamlit as st

with st.sidebar:
    st.markdown("# Contact Us ✉️")
    st.markdown(
        """              
    Send us an email
    
    Pallav Routh - routh.pallav@gmail.com
    
    Srihari Sridhar -      
                """
    )

st.markdown(
    f"""<h1 style="color:#202a44; font-size:42px; "> Frequently Asked Questions 🙋🏽 </h1>""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    Here are some answers to some general questions on how the app operates and what are the limitations of the app. 
    It also contains important trouble-shooting information. Please reach out to the creators for reporting issue and bugs.
    """
)

with st.expander("**What data does EMPATHY Coach collect?**", expanded=True):
    st.markdown(
        """
        Text here
        """
    )

with st.expander("**How does EMPATHY Coach work behind the scenes?**", expanded=True):
    st.markdown(
        """
        Text here
        """
    )

with st.expander("**How long does it take to go through the stages?**", expanded=True):
    st.markdown(
        """
        Text here 
        """
    )
