from flask import Flask,request
from services.text_summerizer import summarize_text
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
    # print("Keywords:", keywords)
    return "Data stored!"

@app.route("/store_pdf", methods=["POST"])
def store_pdf():
    from services.pdf_to_text import extract_pdf_to_text
    pdf_path = request.form.get("pdf_path", "")
    text = extract_pdf_to_text(pdf_path)
    summarized = summarize_text(text)
    summarized_text = summarized["summary"]
    print("Summarized Text:", summarized_text)
    return "PDF processed and data stored!"

@app.route("/store_image", methods=["POST"])
def store_image():
    # from services.image_to_text.py import image_to_text
    image_path = request.form.get("image_path", "")
    text = request.form.get("caption", "")
    # text = image_to_text(image_path)
    summarized = summarize_text(text)
    summarized_text = summarized["summary"]
    print("Summarized Text:", summarized_text)
    return "Image processed and data stored!"

@app.route("/store_youtube_info", methods=["POST"])
def store_youtube_info():
    from services.yt_info_extractor import extract_yt_info
    url = request.form.get("url", "")
    yt_info = extract_yt_info(url)
    print("YouTube Video Info:", yt_info)
    return "YouTube info extracted and data stored!"

@app.route("/store_audio", methods=["POST"])
def store_audio():
    from services.audio_to_text import audio_to_text
    audio_path = request.form.get("audio_path", "")
    text = audio_to_text(audio_path)
    summarized = summarize_text(text)
    summarized_text = summarized["summary"]
    print("Summarized Text:", summarized_text)
    return "Audio processed and data stored!"

@app.route("/store_url", methods=["POST"])
def store_url():
    from services.url_to_text import url_to_text
    url = request.form.get("url", "")
    text = url_to_text(url)
    summarized = summarize_text(text)
    summarized_text = summarized["summary"]
    print("Summarized Text:", summarized_text)
    return "URL processed and data stored!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)