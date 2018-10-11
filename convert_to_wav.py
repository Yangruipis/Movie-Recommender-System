import scipy.io.wavfile
import pydub
import os

def get_extension(file_name):
    return file_name.split('.')[-1]

def change_extension_to_wav(file_name):
    array = file_name.split('.')
    return ".".join(array[0:len(array) - 1] + ["wav"])

def change_extension(file_name, ext):
    array = file_name.split('.')
    return ".".join(array[0:len(array) - 1] + [ext])

video_ext = set(['mp4', 'webm', 'mkv'])

def get_file_list(file_path):
    file_list = [ ]
    for f in os.listdir(file_path):
        if get_extension(f) in video_ext:
            file_list.append(f)
    return file_list

def convert_all(file_path, out_path):
    file_list = get_file_list(file_path)
    for f in file_list:
        print(f)
        sound = pydub.AudioSegment.from_file(file_path + f)
        sound.export(out_path + change_extension_to_wav(f),
            format = "wav", bitrate = "192k")

def convert_by_ffmpeg(file_path, out_path):
    file_list = get_file_list(file_path)
    for f in file_list:
        print(f)
        dest = out_path + change_extension(f, "wav")
        text = 'ffmpeg -i "{0}" "{1}"'
        command = text.format(file_path + f, dest)
        print(command)
        os.system(command)

convert_by_ffmpeg("trailers/", "sound/")
print("finished!")
