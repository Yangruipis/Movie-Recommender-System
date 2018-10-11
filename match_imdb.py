import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_columns = 9999
movies_df = pd.read_csv("ml-20m/movies.csv")
imdb_titles = pd.read_csv("imdb/title.basics.tsv", sep = "\t")
links_df = pd.read_csv("ml-20m/links.csv")
crew_df = pd.read_csv("imdb/title.crew.tsv", sep = "\t")
names_df = pd.read_csv("imdb/name.basics.tsv", sep = "\t")

def match_imdb_titles_basic(links_df, imdb_titles):
    imdb_id_set = set(links_df["imdbId"].tolist())
    filter_column = [ ]
    for item in imdb_titles["tconst"]:
        if int(item[2:]) in imdb_id_set:
            filter_column.append(True)
        else:
            filter_column.append(False)
    imdb_titles_basic = imdb_titles[filter_column]
    imdb_titles_basic.to_csv(
            "data/imdb_titles_basic.tsv", 
            index = False, sep = "\t")

def get_movie_id_imdb_table(links_df):
    table = { }
    for i in range(len(links_df)):
        table[links_df["imdbId"].iloc[i]] = links_df["movieId"].iloc[i]
    return table

def match_imdb_names(links_df, crew_df):
    imdb_id_set = set(links_df["imdbId"].tolist())
    filter_column = [ ]
    for item in crew_df["tconst"]:
        if int(item[2:]) in imdb_id_set:
            filter_column.append(True)
        else:
            filter_column.append(False)
    imdb_crew = crew_df[filter_column]
    imdb_crew.to_csv("data/imdb_crew.tsv",
                     index = False, sep = "\t")

def match_imdb_principals(links_df, imdb_principals):
    imdb_id_set = set(links_df["imdbId"].tolist())
    filter_column = [ ]
    for item in imdb_principals["tconst"]:
        if int(item[2:]) in imdb_id_set:
            filter_column.append(True)
        else:
            filter_column.append(False)
    imdb_principals[filter_column].to_csv(
            "data/imdb_principals.tsv",
            index = False, sep = "\t")

match_imdb_titles_basic(links_df, imdb_titles)
match_imdb_names(links_df, crew_df)
imdb_crew = pd.read_csv("data/imdb_crew.tsv", sep = "\t")
imdb_principals = pd.read_csv("imdb/title.principals.tsv", sep = "\t")
match_imdb_principals(links_df, imdb_principals)

imdb_names = pd.read_csv("imdb/name.basics.tsv", sep = "\t")