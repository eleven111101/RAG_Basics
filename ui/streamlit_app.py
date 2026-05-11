import os
import requests
import streamlit as st

UPLOAD_DIR = "data/docs"

API_URL = "http://127.0.0.1:8000/ask"
INGEST_URL = "http://127.0.0.1:8000/ingest"

st.set_page_config(
    page_title="RAG QnA Bot",
    layout="wide"
)

st.title("RAG QnA Bot")

# =========================
# FILE UPLOAD
# =========================

st.header("Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for uploaded_file in uploaded_files:

        save_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )

        with open(save_path, "wb") as f:

            f.write(uploaded_file.getbuffer())

    st.success("Files Uploaded Successfully")

# =========================
# INGESTION
# =========================

if st.button("Run Ingestion Pipeline"):

    with st.spinner("Creating Vector DB..."):

        response = requests.post(INGEST_URL)

        if response.status_code == 200:

            st.success("Vector DB Created Successfully")

        else:

            st.error("Ingestion Failed")

# =========================
# QUERY
# =========================

st.header("Ask Questions")

query = st.text_input("Enter your question")

if st.button("Ask Question"):

    if query.strip() == "":

        st.warning("Please Enter Question")

    else:

        with st.spinner("Generating Answer..."):

            response = requests.post(
                API_URL,
                json={
                    "question": query
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.subheader("Answer")

                st.write(data["answer"])

                with st.expander("Retrieved Context"):

                    for doc in data["context"]:

                        st.write(doc)
                        st.write("---")

            else:

                st.error("Query Failed")