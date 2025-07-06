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
