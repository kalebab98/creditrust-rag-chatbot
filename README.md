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
| `vector_store/`  | Prebuilt ChromaDB collection of complaint document embeddings.     |

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

---


```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```


