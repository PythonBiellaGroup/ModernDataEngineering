import streamlit as st


def app():
    st.title("Python Biella Group")
    st.subheader("Streamlit webapp")

    st.markdown(
        """
        This is a simple dashboard designed with the new version of streamlit that aim to analyze the sentiment and the text of tweets regarding Apple Airtag.
        
        
        **Streamlit** is now mature and at the 1.1.0 version! (and more)
        - Streamlit webpage: https://blog.streamlit.io/announcing-streamlit-1-0/
        - Documentation: https://docs.streamlit.io/library/get-started
        """
    )

    # st.image(
    #     "./app/static/images/airtag.png",
    #     width=800,
    # )
    st.image("./app/static/images/data_flow.png", width=800)
