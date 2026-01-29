from summa import summarizer, keywords


def summarize_text(text):
    return {
        "summary":summarizer.summarize(text, ratio=0.2),
        "keywords":keywords.keywords(text)
    }
# print(keywords.keywords(text))

# with open("../output/summarized_text.txt", "w", encoding="utf-8") as f:
#     f.write(summarizer.summarize(text, ratio=0.2))
