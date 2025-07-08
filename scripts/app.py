import os
import streamlit as st
import subprocess
import sys
from sentence_transformers import SentenceTransformer
from transformers import pipeline


# --- Colab/Cloud Setup: Download files from Google Drive if not present ---
def download_if_missing(filename, file_id):
    if not os.path.exists(filename):
        import subprocess
        subprocess.run(["pip", "install", "gdown"])
        import gdown
        print(f"Downloading {filename} from Google Drive...")
        gdown.download(id=file_id, output=filename, quiet=False)

# Download aa.py if missing (replace with your actual file ID)
download_if_missing("aa.py", "1t3MI3sjyl4bBx54zfsz3FT40U0W9i1z6")

download_if_missing("requirements.txt", "1wXF__yA63nolHDxy4Pyxfj0SahnjZcGu")


requirements_path = "requirements.txt"


if not os.path.exists("vector_store"):
    download_if_missing("vector_store.zip", "1JJGDAfom94kxFZfV4R49pEAjrvulVetJ")
    import zipfile
    os.makedirs("vector_store", exist_ok=True)
    with zipfile.ZipFile("vector_store.zip", "r") as zip_ref:
        zip_ref.extractall("vector_store")


from task3 import answer_question  # Now safe to import

st.set_page_config(page_title="CrediTrust Complaint RAG Chatbot", layout="centered")
st.title("CrediTrust Complaint RAG Chatbot")
st.write("Ask a question about customer complaints. The AI will answer using real complaint data.")

if 'history' not in st.session_state:
    st.session_state['history'] = []

with st.form(key='chat_form'):
    user_question = st.text_input("Your question:", "")
    submit = st.form_submit_button("Ask")
    clear = st.form_submit_button("Clear")

if clear:
    st.session_state['history'] = []
    st.experimental_rerun()

if submit and user_question.strip():
    with st.spinner("Retrieving answer..."):
        answer, sources, metadatas, distances = answer_question(user_question)
        st.session_state['history'].append({
            'question': user_question,
            'answer': answer,
            'sources': sources
        })

for entry in reversed(st.session_state['history']):
    st.markdown(f"**You:** {entry['question']}")
    st.markdown(f"**AI:** {entry['answer']}")
    with st.expander("Show sources"):
        for i, src in enumerate(entry['sources'][:2]):
            st.markdown(f"**Source {i+1}:** {src}")

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(["This is a test sentence."])
print(embeddings)

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",  # About 300MB download
    device_map="auto"
)