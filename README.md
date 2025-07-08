# 🧠 CrediTrust Complaint Insight Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built to help product, support, and compliance teams at CrediTrust Financial understand customer complaints in real-time.

This AI-powered assistant enables plain-English querying of customer complaint narratives, instantly revealing trends, issues, and insights across five major financial products.

---

## 📊 Business Objective

CrediTrust receives thousands of unstructured complaints every month. Internal teams struggle to extract actionable insights, often spending hours manually sifting through feedback.

This tool reduces that process from **days to minutes**, enabling non-technical stakeholders to:

- Identify major pain points across Credit Cards, Personal Loans, BNPL, Savings Accounts, and Money Transfers.
- Ask natural-language questions like:
  > "What are the top issues in BNPL this month?"

- Get **evidence-backed summaries** powered by LLMs and real complaint data.

---

## ⚙️ Architecture Overview

This project uses **Retrieval-Augmented Generation (RAG)**:

1. **Text Preprocessing** – Clean complaint narratives and filter by product.
2. **Text Chunking** – Break long narratives into semantic chunks.
3. **Vector Embedding** – Use `sentence-transformers/all-MiniLM-L6-v2` for semantic encoding.
4. **Vector Store** – Store and search using `FAISS` or `ChromaDB`.
5. **RAG Pipeline** – Retrieve top-k relevant chunks, send to LLM with prompt.
6. **Chat Interface** – Query the system via a user-friendly UI built with Gradio or Streamlit.

---

## 🧹 Preprocessing Pipeline

### ✅ Initial Cleaning
- Loaded full dataset with `pandas`
- Identified and handled missing values:
  - `Consumer complaint narrative`: **6.6M missing**
  - `Tags`, `Consent`, `Public response`: heavily sparse

### 🔍 Filtering Criteria
- Selected rows where:
  - `Product` is in:
    ```
    ['Credit card', 'Personal loan', 'Buy Now, Pay Later (BNPL)', 'Savings account', 'Money transfers']
    ```
  - `Consumer complaint narrative` is **not null**

### 🧼 Text Cleaning
- Lowercased all narratives
- Removed punctuation, newlines, and extra spaces
- Calculated word counts per narrative (`narrative_length`)

### 📤 Output
- Saved cleaned and filtered data to:
  - `filtered_complaints.csv` (~200 MB)
- Total filtered rows: **~2.9M**

---

## 📊 Key Insights

### 📌 Top Products
| Product                                | Count     |
|----------------------------------------|-----------|
| Credit reporting (various categories)  | 7M+       |
| Debt collection                        | 799k      |
| Mortgage, Checking, Credit card        | 200k–400k |

### ✍️ Narrative Length Stats
- **Mean:** ~55 words
- **Max:** 6,469 words
- **Short entries (≤1 word):** Very common
- **Distribution:** Long-tailed

---

## 🧠 Embedding Pipeline (Task 2)

### 🛠️ Tools & Libraries
- `pandas`, `sentence-transformers`, `langchain`, `chromadb`, `tqdm`
- Model: `all-MiniLM-L6-v2`
- Text splitter: `RecursiveCharacterTextSplitter` (chunk size: 200, overlap: 40)

### 📦 Process
1. Loaded `filtered_complaints.csv` in chunks (1000 rows at a time)
2. For each narrative:
   - Split into overlapping chunks
   - Embedded using sentence-transformer
   - Stored embeddings in ChromaDB collection `complaints`
3. Vector store persisted locally as `./vector_store/`

### ✅ Backup
- Zipped vector store: `vector_store.zip` (~1 GB)
- Copied to Google Drive for long-term storage

---

## ✅ Outputs

| File Name               | Description                          | Size     |
|-------------------------|--------------------------------------|----------|
| `filtered_complaints.csv` | Cleaned complaints data              | ~200 MB  |
| `vector_store/`         | Embedded vector database (ChromaDB)  | ~1 GB    |
| `vector_store.zip`      | Zipped backup of vector store        | ~1 GB    |

---
# 🧠 Task 3: Core RAG Implementation with Prompt Engineering

## 📌 Overview

This task implements the core **Retrieval-Augmented Generation (RAG)** system that answers questions using real-world customer complaint data. The system retrieves the most relevant complaint excerpts using dense embeddings and combines them with a prompt to generate human-readable answers using a text generation model.

---

## 🛠️ Features

- 🔍 **Embedding-based Retrieval** using `all-MiniLM-L6-v2` via `sentence-transformers`
- 🧠 **Prompt Engineering** to guide `google/flan-t5-small` in structured question answering
- 💬 **Context-aware Answer Generation** using HuggingFace Transformers
- ✅ **Qualitative Evaluation Function** to test against multiple financial complaint queries
- 🔒 **Robust error handling** for ChromaDB and model failures

---

## 📁 Folder Structure

```
.
├── task3.py                # Main RAG system logic
├── vector_store/           # Pre-generated embeddings stored by ChromaDB
├── requirements.txt        # Python dependencies
```

---

## ⚙️ Requirements

Install all dependencies:

```bash
pip install -r requirements.txt
```

> 🧠 Note: Models will be automatically downloaded from HuggingFace on first run.

---

## 💡 How It Works

- **Query Embedding**  
  The user’s question is converted to an embedding using `SentenceTransformer`.

- **Vector Search**  
  ChromaDB retrieves the most relevant complaint text chunks based on the query.

- **Prompt Construction**  
  Retrieved chunks are inserted into a prompt that provides instructions to the LLM.

- **Answer Generation**  
  The `flan-t5-small` model generates an answer using the custom prompt.

---

## 🧪 Evaluation

The script includes a function `evaluate_rag_system()` to run a set of pre-defined financial service-related questions. Output includes:

- ✅ Generated Answer  
- 📚 Source Text Chunks  
- 📝 Manual Evaluation Fields (`Quality Score`, `Comments`)

---

# 💬 Task 4: Interactive Chat Interface for RAG System

## 📌 Project Title:
**CrediTrust Complaint Chatbot – Streamlit UI for Retrieval-Augmented Generation**

---

## 🧠 Overview

This task implements a user-friendly **Streamlit-based interface** that allows non-technical users to interact with the **Retrieval-Augmented Generation (RAG)** system developed in Task 3. The chatbot enables users to ask questions about customer complaints and receive grounded, explainable responses.

---

## 🎯 Features

| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| 📝 Text Input Box           | Users type in any question related to financial complaints.                 |
| 🔍 Ask Button               | Triggers the RAG system to fetch and generate an answer.                    |
| 💬 AI Answer Display        | Shows the LLM-generated response based on real complaint data.              |
| 📚 Source Viewer            | Displays the top retrieved complaint chunks used to generate the answer.    |
| ♻️ Clear Button             | Clears the chat history to restart the conversation.                        |
| ⚡ Token-by-token Streaming | *(Optional)* Future enhancement for real-time response generation.          |

---

## 🖼️ Sample UI

```
+-----------------------------------------------------+
| CrediTrust Complaint Chatbot                        |
|-----------------------------------------------------|
| Your question: [ Why are people unhappy with BNPL? ]|
| [ Ask ] [ Clear ]                                   |
|                                                     |
| You: Why are people unhappy with BNPL?              |
| AI: Many users complain about hidden fees...        |
|                                                     |
| ▼ Show sources                                      |
|  - Source 1: "I signed up for BNPL but..."          |
|  - Source 2: "They didn't disclose repayment terms" |
+-----------------------------------------------------+
```

---

## 📁 Folder Structure

```
.
├── app.py                    # Streamlit chatbot app
├── task3.py                  # Core RAG system
├── vector_store/             # ChromaDB vector index
├── requirements.txt          # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

---

## 🔗 Key Components

| Component       | Purpose                                                             |
|------------------|---------------------------------------------------------------------|
| `task3.py`       | Provides `answer_question()` using retrieval + LLM generation.     |
| `app.py`         | Streamlit frontend to collect input, show output, and display sources. |

---

## 💡 How It Works

1. **User types a question.**  
2. **The app calls `answer_question()` from Task 3.**  
3. **The RAG system retrieves relevant chunks and builds a prompt.**  
4. **The LLM generates a contextual answer.**  
5. **Sources used in the response are shown for verification.**

---

## 🚀 Optional Enhancements

- ✅ Token Streaming for more dynamic output *(not yet implemented)*  
- 📊 Score answers based on confidence or source rank  
- 🧪 Feedback box for real-time user evaluation  

```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```



