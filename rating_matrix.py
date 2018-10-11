import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matrix_factorization_utilities as MF

pd.options.display.max_columns = 9999
pd.set_option('display.max_columns', None)  
df = pd.read_csv("data/ratings_2013.csv")

def convert_list(sequence, converter):
    result = []
    for item in sequence:
        result.append(converter(item))
    return result

def plot_user_record(df):
    table = { }
    users = df["userId"].tolist()
    years = df["year"].tolist()
    for year in df["year"].unique():
        table[year] = set()
    for i in range(len(df)):
        (user, year) = (users[i], years[i])
        table[year].add(user)
    year_list = df["year"].unique().tolist()
    year_list.sort()
    user_count = [len(table[year]) for year in year_list]
    frame = pd.DataFrame({
            "year": year_list, "user_count": user_count})
    frame = frame[["year", "user_count"]]
    frame.to_csv("data/user_count_2013.csv", index = False)
#    sns.lineplot(x = "year", y = "user_count", data = frame)
    plt.plot(convert_list(year_list, str), user_count)
#    locs, labels = plt.xticks()
#    plt.setp(labels, rotation=45)
    plt.savefig("figures/user_count.pdf")
    
def leaderboard_by_average_rating(df):
    movies = df["movieId"].unique().tolist()
    table = { }
    movie_list = df["movieId"].tolist()
    rating_list = df["rating"].tolist()
    for movie in movies:
        table[movie] = [ ]
    for i in range(len(df)):
        (movie, rating) = (movie_list[i], rating_list[i])
        table[movie].append(rating)
    movies = list(table.keys())
    num_of_obs = [len(table[movie]) for movie in movies]
    avg_ratings = [np.mean(table[movie]) for movie in movies]
    data = pd.DataFrame(
            list(zip(movies, avg_ratings, num_of_obs)),
            columns = ["movieId", "avg_rating", "num_of_obs"])
    data.to_csv("data/movie_2013_avg_rating.csv")
    return data

def bayesian_average_rating(C, m, rating_df):
    total = rating_df["avg_rating"] * rating_df["num_of_obs"]
    num_votes = rating_df["num_of_obs"]
    bayesian_df = rating_df.copy()
    bayesian_df["bayesian_average_rating"] = ((C * m) + total) / (C + num_votes)
    bayesian_df.to_csv(
            "data/movie_bayesian_average_rating_2013.csv", 
            index = False)
    return bayesian_df

def attach_movie_names(df):
    def movie_table(name_df):
        movie_id = name_df["movieId"].tolist()
        names = name_df["title"].tolist()
        table = { }
        for i in range(len(name_df)):
            table[movie_id[i]] = names[i]
        return table
    name_df = pd.read_csv("ml-20m/movies.csv")
    table = movie_table(name_df)
    names = [ ]
    movie_id = df["movieId"].tolist()
    for item in movie_id:
        names.append(table[item])
    df["title"] = names

def generate_latex_of_rating(df, C = 5000):
    def attach_numbers(frame):
        frame = frame.copy()
        rank = list(range(1, len(frame) + 1))
        frame["rank"] = rank
        return frame
    rating_df = leaderboard_by_average_rating(df)
    rating_df = rating_df.sort_values(
            "avg_rating", ascending = False)
    attach_movie_names(rating_df)
    columns = ["rank", "title", "avg_rating", "num_of_obs"]
    print(attach_numbers(rating_df.head(10))[columns].to_latex(index = False))
    m = df["rating"].mean()
    columns.append("bayesian_average_rating")
    bayesian_df = bayesian_average_rating(C, m, rating_df)
    bayesian_df = bayesian_df.sort_values(
            "bayesian_average_rating", ascending = False)
    print(attach_numbers(bayesian_df.head(10))[columns].to_latex(index = False))
    
def low_rank_approximation(df):
    rating_matrix = pd.pivot_table(
            df, index = "userId", columns = "movieId",
            aggfunc = np.max)
    (U, M) = MF.low_rank_matrix_factorization(
            rating_matrix.as_matrix(),
            num_features = 20,
            regularization_amount = 0.1)
    predicted_ratings = np.matmul(U, M)
    predicted_ratings_df = pd.DataFrame(
            index = df["userId"],
            columns = df["movieId"],
            data = predicted_ratings)
    predicted_ratings_df.to_csv(
            "data/predicted_ratings.csv", index = False)
low_rank_approximation(df)
