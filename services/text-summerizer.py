from summa import summarizer, keywords
with open("../output/transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()
# text = """"""
# print(text)
# print(summarizer.summarize(text))

print(keywords.keywords(text))

with open("../output/summarized_text.txt", "w", encoding="utf-8") as f:
    f.write(summarizer.summarize(text, ratio=0.2))
