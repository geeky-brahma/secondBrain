from flask import Flask,request
from services import audio_to_text
from services.text_summerizer import summarize_text
from embeddings.embedderer import embed_and_store_documents, query_relevant_documents
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
@app.route("/store_text", methods=["POST"])
def store_text():
    text = request.form.get("text", "")
    # Logic to store the text data
    summarized = summarize_text(text)
    # keywords = summarized["keywords"]
    summarized_text = summarized["summary"]
    print("Summarized Text:", summarized_text)
    embed_and_store_documents(text, summarized_text)
    # print("Keywords:", keywords)
    return "Data stored!"

@app.route("/store_pdf", methods=["POST"])
def store_pdf():
    from services.pdf_to_text import extract_pdf_to_text
    pdf_path = request.form.get("pdf_path", "")
    file_name = request.form.get("file_name", "")
    text = extract_pdf_to_text(file_name)
    # summarized = summarize_text(text)
    # summarized_text = summarized["summary"]
    # print("Summarized Text:", summarized_text)
    embed_and_store_documents(file_name, text)
    return "PDF processed and data stored!"

@app.route("/store_image", methods=["POST"])
def store_image():
    # from services.image_to_text.py import image_to_text
    image_path = request.form.get("image_path", "")
    caption = request.form.get("caption", "")
    file_name = request.form.get("file_name", "")
    # summarized = summarize_text(caption)
    # summarized_text = summarized["summary"]
    # print("Summarized Text:", summarized_text)
    embed_and_store_documents(file_name, caption)
    return "Image processed and data stored!"

@app.route("/store_youtube_info", methods=["POST"])
def store_youtube_info():
    from services.yt_info_extractor import extract_yt_info
    url = request.form.get("url", "")
    yt_info = extract_yt_info(url)
    print("YouTube Video Info:", yt_info)
    embed_and_store_documents(url, yt_info)
    return "YouTube info extracted and data stored!"

@app.route("/store_audio", methods=["POST"])
def store_audio():
    from services.audio_to_text import transcribe_audio
    audio_path = request.form.get("audio_path", "")
    file_name = request.form.get("file_name", "")
    text = transcribe_audio(file_name)
    print("Extracted Text from Audio:", text)
    # summarized = summarize_text(text)
    # summarized_text = summarized["summary"]
    # print("Summarized Text:", summarized_text)
    embed_and_store_documents(file_name, text)
    return "Audio processed and data stored!"

@app.route("/store_url", methods=["POST"])
def store_url():
    from services.url_to_text import scrape_url_to_text
    url = request.form.get("url", "")
    text = scrape_url_to_text(url)
    print("Extracted Text from URL:", text)
    # summarized = summarize_text(text)
    # summarized_text = summarized["summary"]
    # print("Summarized Text:", summarized_text)
    embed_and_store_documents(url, text)
    return "URL processed and data stored!"

@app.route("/ask_question", methods=["POST"])
def ask_question():
    question = request.form.get("question", "")
    print(f"Received question: {question}")
    relevant_docs = query_relevant_documents(question)
    print("Relevant Documents:", relevant_docs)
    # Here you would typically use the relevant documents to generate an answer using a language model
    # For demonstration, we'll just return the relevant documents as the "answer"
    # return f"Relevant documents for your question: {relevant_docs}"
    return relevant_docs if relevant_docs else "No relevant documents found."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)