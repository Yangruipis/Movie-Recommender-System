import numpy as np
import pandas as pd
import math
from scipy.sparse.linalg import svds

ratings_df = pd.read_csv("ml-20m/ratings.csv")
print(ratings_df)
R_df = ratings_df.pivot(
    index = "userId",
    columns = "movieId",
    values = "rating").fillna(0)
print(R_df.head())

def make_predictions(R_df, k):
    R = R_df.as_matrix()
    user_ratings_mean = np.mean(R, axis = 1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)
    U, sigma, Vt = svds(R_demeaned, k = k)
    save_matrices(U, sigma, Vt)
    sigma = np.diag(sigma)
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    preds_df = pd.DataFrame(all_user_predicted_ratings, index = R_df.index, columns = R_df.columns)
    return preds_df

def rmse(ratings_df, preds_df):
    users = ratings_df["userId"]
    movies = ratings_df["movieId"]
    ratings = ratings_df["rating"]
    error = 0
    for i in range(len(ratings_df)):
        user = users[i]
        movie = movies[i]
        r = ratings[i]
        r_pred = preds_df[movie][user]
        d = r - r_pred
        error = error + d * d
        if i % 1000000 == 0:
            print(i)
    return math.sqrt(error / len(ratings_df))

def save_matrices(U, sigma, Vt):
   np.savetxt("U.txt", U)
   np.savetxt("sigma.txt", sigma)
   np.savetxt("Vt.txt", Vt)

preds_df = make_predictions(R_df, k = 2000)
RMSE = rmse(ratings_df, preds_df)
print("RMSE = " + str(RMSE))
