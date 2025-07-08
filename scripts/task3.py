# -*- coding: utf-8 -*-
import pandas as pd
from sentence_transformers import SentenceTransformer
import torch
import chromadb
from chromadb.config import Settings
from transformers.pipelines import pipeline

# Device setup
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
GEN_MODEL_NAME = "google/flan-t5-small"  # Smallest real instruction-following model

# Load embedding model
embed_model = SentenceTransformer(EMBED_MODEL_NAME, device=DEVICE)

# Setup ChromaDB
settings = Settings(
    persist_directory="vector_store",
    is_persistent=True
)
chroma_client = chromadb.Client(settings)
try:
    collection = chroma_client.get_collection(name="complaints")
except Exception as e:
    print(f"❌ Failed to load collection: {e}")
    collection = None

# Generator pipeline

def get_generator():
    return pipeline(
        "text2text-generation",
        model=GEN_MODEL_NAME,
        device_map="auto"
    )

generator = get_generator()

# --- RAG Core Logic ---

def retrieve_relevant_chunks(query, top_k=5):
    query_embedding = embed_model.encode([query], device=DEVICE)
    if hasattr(query_embedding, "tolist"):
        query_embedding = query_embedding.tolist()
    if collection is None:
        print("❌ Collection is None. Cannot query.")
        return [], [], []
    try:
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
    except Exception as e:
        print(f"❌ ChromaDB query failed: {e}")
        return [], [], []
    if results is None:
        print("❌ Query returned None results.")
        return [], [], []
    documents = results.get('documents', [[]])
    metadatas = results.get('metadatas', [[]])
    distances = results.get('distances', [[]])
    if not (isinstance(documents, list) and len(documents) > 0 and isinstance(documents[0], list)):
        print("⚠️ Documents not in expected format.")
        return [], [], []
    if not (isinstance(metadatas, list) and len(metadatas) > 0 and isinstance(metadatas[0], list)):
        print("⚠️ Metadatas not in expected format.")
        return [], [], []
    if not (isinstance(distances, list) and len(distances) > 0 and isinstance(distances[0], list)):
        print("⚠️ Distances not in expected format.")
        return [], [], []
    if not documents[0]:
        print("⚠️ No documents found.")
        return [], [], []
    return documents[0], metadatas[0], distances[0]

# Prompt engineering (Task 3 requirement)
def build_prompt(question, context_chunks):
    prompt_template = (
        "You are a financial analyst assistant for CrediTrust. "
        "Your task is to answer questions about customer complaints. "
        "Use the following retrieved complaint excerpts to formulate your answer. "
        "If the context doesn't contain the answer, state that you don't have enough information.\n\n"
        "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    context = "\n".join(context_chunks)
    return prompt_template.format(context=context, question=question)

# Generation

def generate_answer_with_llm(question, context_chunks):
    prompt = build_prompt(question, context_chunks)
    response = generator(prompt, max_length=256)[0]['generated_text']
    return response.strip()

# Main RAG answer function
def answer_question(question, k=5):
    try:
        context_chunks, metadatas, distances = retrieve_relevant_chunks(question, top_k=k)
        if not context_chunks:
            return "No relevant information found.", [], [], []
        answer = generate_answer_with_llm(question, context_chunks)
        return answer, context_chunks, metadatas, distances
    except Exception as e:
        print(f"❌ Exception occurred in answer_question: {e}")
        return "An error occurred.", [], [], []

# Qualitative evaluation (Task 3 requirement)
def evaluate_rag_system():
    evaluation_questions = [
        "Why are people unhappy with BNPL?",
        "What issues are being reported with personal loans?",
        "How can CrediTrust improve its savings account product?",
        "What are common issues with money transfers?",
        "What are the top complaints about credit cards?",
    ]
    results = []
    for q in evaluation_questions:
        answer, sources, metadatas, _ = answer_question(q)
        results.append({
            "Question": q,
            "Generated Answer": answer,
            "Retrieved Sources": sources[:2],
            "Quality Score": None,  # To be filled in after manual review
            "Comments": ""
        })
    df = pd.DataFrame(results)
    print("\nEvaluation Table:")
    print(df.to_markdown(index=False))
    return df

# Main entry point
def main():
    q = "Why are people unhappy with BNPL?"
    a, s, m, d = answer_question(q)
    print("Answer:", a)
    print("Sources:", s[:2])
    print("Metadatas:", m[:2])
    print("Distances:", d[:2])
    # Run evaluation
    evaluate_rag_system()

if __name__ == "__main__":
    main()
