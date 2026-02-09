
from datetime import date
import time
import random
import ollama
import chromadb

def embed_and_store_documents(info, summary):
    #info: Text or document link or image link or youtube link or audio link
    # summary: Summarized text of the info


    # documents = []
    # uid = date.today().strftime("%Y%m%d")+"_"+time.strftime("%H%M%S", time.localtime())+"_"+str(len(string))+"_"+str(random.randint(10000,99999))


    # time.strftime("%H%M%S", time.localtime())

        
    # client = chromadb.Client()
    client = chromadb.PersistentClient(path="./db")
    collection = client.get_or_create_collection(
        name="docs",
        metadata={"hnsw:space": "cosine"}
    )

    # store each chunk in a vector embedding database
    base_uid = (
        date.today().strftime("%Y%m%d")
        + "_"
        + time.strftime("%H%M%S", time.localtime())
        + "_"
        + str(len(info))
        + "_"
        + str(random.randint(10000, 99999))
    )

    # chunk by lines, fallback to sentence-like chunks
    raw_chunks = [line.strip() for line in summary.splitlines() if line.strip()]
    if not raw_chunks:
        raw_chunks = [s.strip() for s in summary.replace("\n", " ").split(". ") if s.strip()]

    # merge small chunks to reduce overly tiny fragments
    chunks = []
    buffer = ""
    for part in raw_chunks:
        if len(buffer) + len(part) + 1 <= 300:
            buffer = f"{buffer} {part}".strip()
        else:
            if buffer:
                chunks.append(buffer)
            buffer = part
    if buffer:
        chunks.append(buffer)

    for idx, chunk in enumerate(chunks):
        uid = f"{base_uid}_{idx}"
        response = ollama.embed(model="mxbai-embed-large", input=chunk)
        embeddings = response["embeddings"][0]  # Extract first embedding
        collection.add(
            ids=[uid],
            embeddings=[embeddings],  # Wrap in list for ChromaDB
            documents=[chunk],  # Store chunk text for retrieval
            metadatas=[{"source": info, "summary_chunk": chunk}],
        )
        print(f"Added chunk {idx + 1}/{len(chunks)} for {info} with UID: {uid}")


def query_relevant_documents(query):
    # query: A question or statement to find relevant documents for

    # client = chromadb.Client()
    client = chromadb.PersistentClient(path="./db")
    collection = client.get_or_create_collection(
        name="docs",
        metadata={"hnsw:space": "cosine"}
    )

    response = ollama.embed(model="mxbai-embed-large", input=query)
    query_embedding = response["embeddings"][0]  # Extract first embedding
    print("Test Query:", query)
    results = collection.query(
        query_embeddings=[query_embedding],  # Wrap in list for ChromaDB
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )
    print(f"Query: {query}\nResults: {results}\n")

    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    keep_indices = [i for i, d in enumerate(distances) if d < 0.8]  # Keep results with distance < 0.8

    filtered_results = {
        # "ids": [[ids[i] for i in keep_indices]],
        # "documents": [[documents[i] for i in keep_indices]],
        "metadatas": [[metadatas[i] for i in keep_indices]],
        # "distances": [[distances[i] for i in keep_indices]],
    }
    print(f"Filtered Results (distance < 0.8): {filtered_results}\n")
    return filtered_results['metadatas'][0][0]['source'] if filtered_results['metadatas'] else []

# print(query_relevant_documents("Summer day"))

# an example input
# input = "how to be a llama expert"

# # generate an embedding for the input and retrieve the most relevant doc
# response = ollama.embed(
#     model="mxbai-embed-large",
#     input=input
# )
# results = collection.query(
#     query_embeddings=[response["embeddings"][0]],  # Extract first embedding
#     n_results=3
#     # n_results=1
# )
# # data = results['documents'][0][0] if results['documents'] else "No relevant document found."
# # print("Most relevant document:", results["ids"][0][0])
# print(results)
# with open('../temp/retrieved_docs.json', 'w', encoding='utf-8') as f:
#     import json
#     json.dump(results, f, ensure_ascii=False, indent=4)