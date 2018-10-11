import cv2
import matplotlib.pyplot as plt
import os
import os.path
import pandas as pd

def count_hsv(h_data, s_data, v_data, image):
    nRows, nCols, _ = image.shape
    for row in range(nRows):
        for col in range(nCols):
            H = image[row, col, 0]
            S = image[row, col, 1]
            V = image[row, col, 2]
            h_data[H] += 1
            s_data[S] += 1
            v_data[V] += 1
    
def init_table():
    data = { }
    for i in range(256):
        data[i] = 0
    return data

def FrameCapture(path):
    videoObj = cv2.VideoCapture(path)
    count = 0
    success = True
    while success:
        sucess, image = videoObj.read()
#        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#        count_hsv(h_data, s_data, v_data, hsv_image)
#        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
#        cv2.imwrite("frames/frame%d.jpg" % count, image)
        print(count)
        count += 1
        
def list_jpg_files(path):
    files = [ ]
    for file in os.listdir(path):
        if len(file) > 4 and file[-4:] == ".jpg":
            files.append(file)
    return files

#    L = cv2.calcHist(lab_list, [0], None, [256], [0, 256])
#    plt.plot(L, color = "red")
#    plt.show()
#    A = cv2.calcHist(lab_list, [1], None, [256], [0, 256])
#    plt.plot(A, color = "red")
#    plt.show()
#    B = cv2.calcHist(lab_list, [2], None, [256], [0, 256])
#    plt.plot(B, color = "red")
#    plt.show()
def process_all_images(folder):
    files = list_jpg_files(folder)
    hsv_list = [ ]
    lab_list = [ ]
    
    for file in files:
        image = cv2.imread(folder + "/" + file)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        hsv_list.append(hsv_image)
        lab_list.append(lab_image)
    H = cv2.calcHist(hsv_list, [0], None, [180], [0, 180])
    # (256, 1)
    plt.plot(H)
    plt.show()
    S = cv2.calcHist(hsv_list, [1], None, [256], [0, 256])
    plt.plot(S)
    plt.show()
    V = cv2.calcHist(hsv_list, [2], None, [256], [0, 256])
    plt.plot(V)
    plt.show()
    
def extract_images(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
      success,image = vidcap.read()
      # print ('Read a new frame: ', success)
      cv2.imwrite(pathOut + "frame%d.jpg" % count, image)     # save frame as JPEG file
      count = count + 1

video_ext = set(['mp4', 'webm', 'mkv'])

def get_extension(file_name):
    return file_name.split('.')[-1]

def get_file_list(file_path):
    file_list = [ ]
    for f in os.listdir(file_path):
        if get_extension(f) in video_ext:
            file_list.append(f)
    return file_list

def filter_links():
    youtube_links = pd.read_csv("ml-20m-youtube/ml-youtube.csv")
    links = youtube_links["youtubeId"].tolist()
    path = "/run/media/heyanjie/Seagate Backup Plus Drive/trailers"
    file_list = get_file_list(path)
    link_set = set()
    for f in file_list:
        link = get_link(f)
        link_set.add(link)
    fc = [ ]
    for link in links:
        fc.append(link in link_set)
    return youtube_links[fc]

def get_link(file_name):
    return file_name.split('-')[-1].split('.')[0]

def remove_large_videos(youtube_links):
    trailers_duration = pd.read_csv("data/trailers_less_than_10min.csv")
    movie_id_set = set(trailers_duration["movieId"].tolist())
    src_path = "/run/media/heyanjie/Seagate Backup Plus Drive/trailers/"
    table = make_link_table(youtube_links)
    dest_path = "/run/media/heyanjie/Seagate Backup Plus Drive/large_videos/"
    for f in get_file_list(src_path):
        link = get_link(f)
        movie = table[link]
        if not movie in movie_id_set:
            os.rename(src_path + f, dest_path + f)
    
def make_link_table(youtube_links):
    table = { }
    links = youtube_links["youtubeId"].tolist()
    movies = youtube_links["movieId"].tolist()
    for i in range(len(links)):
        table[links[i]] = movies[i]
    return table

def extract_all(youtube_links):
    src_path = "/run/media/heyanjie/Seagate Backup Plus Drive/trailers/"
    dest_path = "/run/media/heyanjie/Seagate Backup Plus Drive/trailer_frames/"
    table = make_link_table(youtube_links)
    count = 0
    for f in get_file_list(src_path):
        link = get_link(f)
        movie = table[link]
        os.mkdir(dest_path + str(movie))
        extract_images(src_path + f,
                       dest_path + str(movie) + "/")
        count += 1
        print("count = " + str(count) + ", trailer = " + f)
            
def extract_all_multi_processing(youtube_links):
    src_path = "/run/media/heyanjie/Seagate Backup Plus Drive/trailers/"
    dest_path = "/run/media/heyanjie/Seagate Backup Plus Drive/trailer_frames/"
    table = make_link_table(youtube_links)
    count = 0
    for f in get_file_list(src_path):
        link = get_link(f)
        movie = table[link]
        os.mkdir(dest_path + str(movie))
        text = "python3 extract_images_from_one_video.py --pathIn \"{0}\" --pathOut \"{1}\" &"
        command = text.format(src_path + f,
                       dest_path + str(movie) + "/")
        os.system(command)
        count += 1
        if count % 1000 == 0:
            print(count)

youtube_links = filter_links()
print(youtube_links.shape)
extract_all(youtube_links)
print("finished!")
