# -*- coding: utf-8 -*-
pip install pandas sentence-transformers chromadb langchain tqdm

from google.colab import drive
drive.mount('/content/drive')

DATA_PATH = '/content/drive/MyDrive/filtered_complaints.csv'

import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import torch
from tqdm import tqdm
import os


chunk_size = 1000
chunk_counter = 0
model_name = "all-MiniLM-L6-v2"
batch_size = 64

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")
model = SentenceTransformer(model_name, device=device)

settings = Settings(
    persist_directory="vector_store",
    is_persistent=True
)
chroma_client = chromadb.Client(settings)
collection = chroma_client.get_or_create_collection(name="complaints")

splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)

for chunk_num, df_chunk in enumerate(pd.read_csv(DATA_PATH, chunksize=chunk_size)):
    print(f"Processing chunk {chunk_num + 1} ({len(df_chunk)} complaints)...")
    batch_chunks = []
    batch_metadatas = []
    batch_ids = []
    for idx, row in df_chunk.iterrows():
        narrative = str(row['Consumer complaint narrative']) if pd.notna(row['Consumer complaint narrative']) else ""
        if narrative.strip():
            text_chunks = splitter.split_text(narrative)
            for text_chunk in text_chunks:
                batch_chunks.append(text_chunk)
                batch_metadatas.append({
                    'complaint_id': str(idx),
                    'product': str(row['Product']),
                    'issue': str(row['Issue']),
                    'date_received': str(row['Date received'])
                })
                batch_ids.append(f"chunk_{chunk_counter}")
                chunk_counter += 1
    if batch_chunks:
        print(f"Embedding {len(batch_chunks)} chunks...")
        for i in range(0, len(batch_chunks), batch_size):
            end_idx = min(i + batch_size, len(batch_chunks))
            chunk_batch = batch_chunks[i:end_idx]
            embeddings = model.encode(chunk_batch, batch_size=batch_size, show_progress_bar=False, device=device)
            collection.add(
                documents=chunk_batch,
                embeddings=embeddings,
                metadatas=batch_metadatas[i:end_idx],
                ids=batch_ids[i:end_idx]
            )
        print(f"Added {len(batch_chunks)} chunks to vector store")

del chroma_client
print("Done! Vector store is in ./vector_store/")

import shutil
shutil.make_archive('vector_store', 'zip', 'vector_store')
shutil.copy('vector_store.zip', '/content/drive/MyDrive/vector_store.zip')
print("Vector store zip copied to Google Drive!")