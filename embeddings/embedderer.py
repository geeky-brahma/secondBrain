# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# sentences = [
#     "What is Artificial Intelligence?",
#     "How do you cook spaghetti pasta?",
#     "Basics of machine learning and data science",
#     "Python is a versatile programming language",
#     "Deep learning is a subfield of machine learning",
#     "Best practices for cooking Italian food",
#     "Guide to AI tools and frameworks",
#     "Natural language processing with Transformers",
#     "Introduction to neural networks",
#     "Steps to make pasta carbonara",
#     "data science roadmap",
#         "data science roadmap for beginners",
#         "complete data science roadmap",
#         "how to become data scientist",
#         "learn data science roadmap",
#         "data science for beginners",
#         "how to become a data scientist",
#         "code with mosh",
#         "programming with mosh",
#         "mosh hamedani",
#         "data science",
#         "tech career",
#         "data scientist roadmap",
#         "data science learning path",
#         "tech skills",
#         "career development",
#         "learn data science",
#         "data engineer",
#         "how to learn data science",
#         "machine learning"
# ]

# model = SentenceTransformer('all-MiniLM-L6-v2')
# sentence_embeddings = model.encode(sentences).astype('float32')

# dimension = sentence_embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)
# index.add(sentence_embeddings)

# query = input("Enter your query: ")
# query_embedding = model.encode([query]).astype('float32')

# k = 3
# distances, indices = index.search(query_embedding, k)

# print("\n Top matching sentences:")
# for i, idx in enumerate(indices[0]):
#     print(f"{i+1}. {sentences[idx]} (Distance: {distances[0][i]:.4f})")





from datetime import date
import time
import random
import ollama
import chromadb

list = ["What is Artificial Intelligence?",
    "How do you cook spaghetti pasta?",
    "Basics of machine learning and data science",
    "Python is a versatile programming language",
    "Deep learning is a subfield of machine learning",
    "Best practices for cooking Italian food",
    "Guide to AI tools and frameworks",
    "Natural language processing with Transformers",
    "Introduction to neural networks",
    "Steps to make pasta carbonara",
    "data science roadmap",
        "data science roadmap for beginners",
        "complete data science roadmap",
        "how to become data scientist",
        "learn data science roadmap",
        "data science for beginners",
        "how to become a data scientist",
        "code with mosh",
        "programming with mosh",
        "mosh hamedani",
        "data science",
        "tech career",
        "data scientist roadmap",
        "data science learning path",
        "tech skills",
        "career development",
        "learn data science",
        "data engineer",
        "how to learn data science",
        "machine learning"]

string = ", ".join(list)

documents = [string,
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
    "Llama experts should have ability to do something crazy like carry 75 pounds for 20 miles",
    "Llama experts should have knowledge on python programming to analyze llama data",
    "Llama need to understand machine learning concepts to improve llama care"
    # "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
    # "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    # "Llamas are vegetarians and have very efficient digestive systems",
    # "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]
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