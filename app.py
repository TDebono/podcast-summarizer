
import streamlit as st

STREAMLIT_maxUploadSize=2000


st.set_page_config(
    page_title="Podscript - Probably the easiest way to transcribe your podcast", page_icon="✍🏼", initial_sidebar_state="expanded"
)

st.title("Podscript - Probably the easiest way to transcribe your podcast ✍🏼")
uploaded_file = st.file_uploader("Upload your podcast audio file")

st.button('Transcribe!')