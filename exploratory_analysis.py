import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import numpy as np
from pandas import Series
from wordcloud import WordCloud

pd.options.display.max_columns = 9999
df = pd.read_csv("ml-20m/ratings.csv")

def count_unique_user_and_movie(df):
    user_count = len(df["userId"].unique())
    movie_count = len(df["movieId"].unique())
    print("user count: " + str(user_count))
    print("movie count: " + str(movie_count))
    return (user_count, movie_count)

def unique_rating(df):
    ratings = df["rating"].unique()
    rating_list = ratings.tolist()
    rating_list.sort()
    return rating_list

def rating_distribution(df):
    plt.hist(df["rating"])
    plt.savefig("figures/rating_distribution.png")
    
def parse_date_from_timestamp(date19700101, seconds):
    date = date19700101 + timedelta(seconds = int(seconds))
    return (date.year, date.month, date.day)

def parse_timestamp_column(df):
    n = len(df)
    timestamp = df["timestamp"]
    date19700101 = datetime(month = 1, day = 1, year = 1970)
    year = np.zeros(n).astype(np.int)
    month = np.zeros(n).astype(np.int)
    day = np.zeros(n).astype(np.int)
    for i in range(n):
        (y, m, d) = parse_date_from_timestamp(
                date19700101, timestamp.iloc[i])
        (year[i], month[i], day[i]) = (y, m, d)
    df["year"] = year
    df["month"] = month
    df["day"] = day

def calculate_average_of_rating_by_year(df):
    avg_rating_df = df.groupby(by = ["year"])["rating"].mean()
    avg_rating_df.to_csv("data/ts_year_ratings.csv", index = False)
    
def plot_ts_year_ratings(df):
    calculate_average_of_rating_by_year(df)
    series = Series.from_csv("data/ts_year_ratings.csv", header = 0)
    series.plot()
    
def movies_genres(movies_df):
    genres = movies_df["genres"]
    result = set()
    for item in genres:
        for i in item.split('|'):
            result.add(i)
    return sorted(list(result))

def plot_genres_word_cloud(movies_df):
    genres = movies_df["genres"]
    words = [ ]
    for item in genres:
        for i in item.split('|'):
            words.append(i)
    text = " ".join(words)
    wordcloud = WordCloud(background_color = "white", width = 1000, height = 860, margin = 2).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file("figures/movies_genres_word_cloud.png")

def count_genres_freq(movies_df):
    genres = movies_df["genres"]
    genres_list = movies_genres(movies_df)
    table = { }
    for item in genres_list:
        table[item] = 0
    for item in genres:
        for i in item.split('|'):
            table[i] += 1
    freq_list = [ ]
    for item in genres_list:
        freq_list.append(table[item])
    pd.DataFrame({"genres": genres_list,
                  "freq": freq_list})[["genres", "freq"]].to_csv(
            "data/genres_freq.csv", index = False
            )
    return (genres_list, freq_list, table)

def plot_hist_genres(movies_df):
    (genres_list, freq_list, table) = count_genres_freq(movies_df)
    plt.bar(genres_list, freq_list, align = "center")
    locs, labels = plt.xticks()
    plt.figure(1, [20, 8])
    plt.setp(labels, rotation=45)
    plt.savefig("figures/genres_hist.png")

def select_ratings_year_after_2013(df):
    data = df[df["year"] >= 2013]
    data.to_csv("data/ratings_2013.csv", index = False)
    return data

count_unique_user_and_movie(df)
unique_rating(df)
rating_distribution(df)
parse_timestamp_column(df)
df.to_csv("data/ratings_with_date.csv", index = False)

df = pd.read_csv("data/ratings_with_date.csv")
movies_df = pd.read_csv("ml-20m/movies.csv")
