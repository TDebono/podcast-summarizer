
import streamlit as st
import config

import requests
from time import sleep

STREAMLIT_maxUploadSize=2000
API_KEY = config.API_KEY


st.set_page_config(
    page_title="Podscript - Probably the easiest way to transcribe your podcast", page_icon="✍🏼", initial_sidebar_state="expanded"
)

st.title("Podscript ✍🏼")
# st.title("blank")
uploaded_file = st.file_uploader("Upload your podcast audio file")

go = st.button('Transcribe!')

if go:

    with st.spinner(text="This might take a while, maybe it's time to grab a coffee ☕"):

        headers = {
            "authorization": API_KEY,
            "content-type": "application/json"
        }

        transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
        upload_endpoint = 'https://api.assemblyai.com/v2/upload'
        
        # make a function to pass the mp3 to the upload endpoint
        def read_file(filename):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(5242880)
                    if not data:
                        break
                    yield data
        # read_file(uploaded_file)
        # upload our audio file
        upload_response = requests.post(
            upload_endpoint,
            headers=headers, data=uploaded_file
        )

        # send a request to transcribe the audio file
        transcript_request = {'audio_url': upload_response.json()['upload_url']}
        transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

        # set up polling
        polling_response = requests.get(transcript_endpoint+"/"+transcript_response.json()['id'], headers=headers)
        filename = transcript_response.json()['id'] + '.txt'

        # if our status isn’t complete, sleep and then poll again
        while polling_response.json()['status'] != 'completed':
            sleep(30)
            polling_response = requests.get(transcript_endpoint+"/"+transcript_response.json()['id'], headers=headers)
            print("File is", polling_response.json()['status'])
        
        final_transcription = polling_response.json()['text']

        st.header("Your transcript is ready!")
        st.subheader("Go ahead and copy the transcript below, or simply download it directly as a text file.\
                    No piece of software is perfect and we are continuously improving our algorithms, so you might want to briefly review the transcript after having downloaded it.\
                    Thanks for your trust and support! 🚀")

        st.write(final_transcription)

        st.download_button(
            label="Download transcript",
            data=final_transcription,
            file_name='transcript.txt'
        )
