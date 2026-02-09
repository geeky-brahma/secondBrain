import json
import yt_dlp

def extract_yt_info(url: str) -> dict:
    URL = url
    # URL = "https://youtube.com/watch?si=_SXsFI8fqcwngzXm&v=j1lTvjmOJbQ"

    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        data = json.dumps(ydl.sanitize_info(info))
        # print("Video Information JSON:", data)
        channel_name = json.loads(data)["channel"] if "channel" in data else "Unknown"
        # print("Channel Name:", channel_name)
        title = json.loads(data)["title"] if "title" in data else "Unknown"
        # print("Title:", title)
        description = json.loads(data)["description"] if "description" in data else "No Description"
        # print("Description:", description)
        # tags = json.loads(data)["tags"] if "tags" in data else []
        # print("Tags:", tags)
        # data = {"channel": channel_name, "title": title, "description": description}
        # print("Extracted Data:", data)
        data = channel_name + " " + title + " " + description
        return data
        

    # with open('../temp/video_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(json.loads(data), f, ensure_ascii=False, indent=4)
