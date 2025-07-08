🧠 Task 3: Core RAG Implementation with Prompt Engineering
📌 Overview
This task implements the core Retrieval-Augmented Generation (RAG) system that answers questions using real-world customer complaint data. The system retrieves the most relevant complaint excerpts using dense embeddings and combines them with a prompt to generate human-readable answers using a text generation model.

🛠️ Features

🔍 Embedding-based Retrieval using all-MiniLM-L6-v2 via sentence-transformers.


🧠 Prompt Engineering to guide google/flan-t5-small in structured question answering.


💬 Context-aware Answer Generation using HuggingFace Transformers.


✅ Qualitative Evaluation Function to test against multiple financial complaint queries.


🔒 Robust error handling for ChromaDB and model failures.


📁 Folder Structure
graphqlCopyEdit

.├── task3.py                # Main RAG system logic
├── vector_store/           # Pre-generated embeddings stored by ChromaDB├── requirements.txt        # Python dependencies

⚙️ RequirementsInstall all dependencies:
bash
CopyEdit
pip install -r requirements.txt

Models will be automatically downloaded from HuggingFace upon first run.
💡 How It Works
Query Embedding:
The user’s question is converted to an embedding using SentenceTransformer.


Vector Search:
ChromaDB retrieves the most relevant complaint text chunks based on the query.


Prompt Construction:
Retrieved chunks are inserted into a prompt that provides instructions to the LLM.


Answer Generation:
The flan-t5-small model generates an answer using the custom prompt.


🧪 Evaluation
The script includes a function evaluate_rag_system() to run a set of pre-defined financial service-related questions. Output includes:

Generated Answer


Source Text Chunks


Manual Evaluation Fields (Quality Score, Comments)


▶️ Running the Scriptbash
CopyEdit
python task3.py

You will see:

An answer to a sample question (e.g., “Why are people unhappy with BNPL?”)


The top source complaint chunks


An evaluation table printed in markdown format


📌 Sample Prompt Template
text
CopyEdit
You are a financial analyst assistant for CrediTrust. Your task is to answer questions about customer complaints.
Use the following retrieved complaint excerpts to formulate your answer.If the context doesn't contain the answer, state that you don't have enough information.
Context:
<retrieved_text>
Question: <user_question>
Answer:
📥 Output Example
sql
CopyEdit
Question: Why are people unhappy with BNPL?
Answer: Many users report frustration due to hidden fees and poor transparency in repayment structures.
Source 1: ... (first document chunk)Source 2: ... (second document chunk)

📎 Notes
If ChromaDB collection is not found or corrupt, retrieval will fail gracefully.


Add new questions to the evaluation_questions list to expand the test suite.


For deployment or further UI integration, see Task 4 (app.py and Streamlit interface).
