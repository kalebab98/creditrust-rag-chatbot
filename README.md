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

