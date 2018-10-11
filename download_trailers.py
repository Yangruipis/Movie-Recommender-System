import pandas as pd
import youtube_dl
pd.options.display.max_columns = 9999
df = pd.read_csv("ml-20m-youtube/ml-youtube.csv")

table = { }
for i in range(len(df)):
    table[df["movieId"].iloc[i]] = df["youtubeId"].iloc[i]
    
def download_video(youtubeId):
    ydl_opts = {
            "noplaylist": True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        link = "https://www.youtube.com/watch?v=" + youtubeId
        ydl.download([link])
        
with open("missing_video_id", "w") as f:
    for youtubeId in df["youtubeId"]:
        try:
            download_video(youtubeId)
        except:
            f.write(youtubeId)
            f.write("\n")