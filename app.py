from flask import Flask,request
from services.text_summerizer import summarize_text
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
@app.route("/store_text", methods=["POST"])
def store_data():
    text = request.form.get("text", "")
    # Logic to store the text data
    summarized = summarize_text(text)
    # keywords = summarized["keywords"]
    summarized_text = summarized["summary"]
    print("Summarized Text:", summarized_text)
    # print("Keywords:", keywords)
    return "Data stored!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)