
from datetime import date
import time
import random
import ollama
import chromadb

def embed_and_store_documents(documents):

    # documents = []
    # uid = date.today().strftime("%Y%m%d")+"_"+time.strftime("%H%M%S", time.localtime())+"_"+str(len(string))+"_"+str(random.randint(10000,99999))


    # time.strftime("%H%M%S", time.localtime())

    # client = chromadb.PersistentClient(path="./db")
    client = chromadb.Client()
    collection = client.create_collection(name="docs")

    # store each document in a vector embedding database
    for i, d in enumerate(documents):
        uid = date.today().strftime("%Y%m%d")+"_"+time.strftime("%H%M%S", time.localtime())+"_"+str(len(d))+"_"+str(random.randint(10000,99999))
        response = ollama.embed(model="mxbai-embed-large", input=d)
        embeddings = response["embeddings"][0]  # Extract first embedding
        collection.add(
        ids=[uid],
        embeddings=[embeddings],  # Wrap in list for ChromaDB
        documents=[d]
        )
        print(f"Added document {d} with UID: {uid}\n")

# an example input
input = "how to be a llama expert"

# generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
    model="mxbai-embed-large",
    input=input
)
results = collection.query(
    query_embeddings=[response["embeddings"][0]],  # Extract first embedding
    n_results=3
    # n_results=1
)
# data = results['documents'][0][0] if results['documents'] else "No relevant document found."
# print("Most relevant document:", results["ids"][0][0])
print(results)
with open('../temp/retrieved_docs.json', 'w', encoding='utf-8') as f:
    import json
    json.dump(results, f, ensure_ascii=False, indent=4)