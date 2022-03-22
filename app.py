
import streamlit as st

st.set_page_config(
    page_title="Podscript - Probably the easiest way to transcribe your podcast", page_icon="✍🏼", initial_sidebar_state="expanded"
)

uploaded_file = st.file_uploader("Upload your podcast audio file")

st.button('Transcribe!')