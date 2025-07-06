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
