from moviepy.editor import VideoFileClip
import os
import pandas as pd

def duration(file_name):
    clip = VideoFileClip(file_name)
    return clip.duration

def duration_by_ffmpeg(file_name):
    text = "ffmpeg -i \"{0}\" 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
    command = text.format(file_name)
    return os.popen(command).readline()

video_ext = set(['mp4', 'webm', 'mkv'])

def get_extension(file_name):
    return file_name.split('.')[-1]

def get_file_list(file_path):
    file_list = [ ]
    for f in os.listdir(file_path):
        if get_extension(f) in video_ext:
            file_list.append(f)
    return file_list

def get_link(file_name):
    return file_name.split('-')[-1].split('.')[0]

def get_all_duration(path):
    file_list = get_file_list(path)
    duration_list = [ ]
    count = 0
    youtube_links = pd.read_csv("data/valid_youtube_links.csv")
    links = youtube_links["youtubeId"]
    movies = youtube_links["movieId"]
    table = { }
    out = open("data/trailers_duration_ffmpeg.csv", "w")
    out.write("movieId,duration\n")
    for i in range(len(links)):
        table[links[i]] = movies[i]
    for f in file_list:
        d = duration_by_ffmpeg(path + f)
        duration_list.append(d)
        link = get_link(f)
        out.write(str(table[link]) + ",")
        out.write(str(d) + "\n")
        count += 1
        print(count)
    out.close()
    return duration_list

def count_seconds(df):
    duration = df["duration"].tolist()
    seconds_list = [ ]
    for d in duration:
        hour, minute, second, ten_millisecond = str(d).replace('.', ':').split(':')
        hour, minute, second, ten_millisecond = int(hour), int(minute), int(second), int(ten_millisecond)
        total_second = hour * 3600 + minute * 60 + second + ten_millisecond * 0.01
        total_second = float(total_second)
        seconds_list.append(total_second)
    df["second"] = seconds_list
duration_list = get_all_duration("/run/media/heyanjie/Seagate Backup Plus Drive/trailers/")
