import pandas as pd

names_df = pd.read_csv("imdb/name.basics.tsv", sep = "\t")

def generate_edges(names_df):
    f = open("data/crew_edges.txt", "w")
    f.write("name,movie\n")
    for i in range(len(names_df)):
        name = names_df["nconst"].iloc[i]
        movies = names_df["knownForTitles"].iloc[i].split(',')
        for movie in movies:
            f.write(name)
            f.write(',')
            f.write(movie)
            f.write('\n')
    f.close()

def have_intersection(set1, set2):
    for item in set1:
        if item in set2:
            return True
    return False

def remove_zero_movie_attendance():
    edges = pd.read_csv("data/crew_edges.txt")
    edges = edges[edges["movie"] != "\\N"]
    edges.to_csv("data/crew_edges.txt", index = False)
    
def filter_edges():
    edges = pd.read_csv("data/crew_edges.txt")
    people = list(set(list(map(lambda name: int(name[2:]),
                edges["name"].tolist()))))
    table = {}
    src = []
    dest = []
    for p in people:
        table[p] = [ ]
    for i in range(len(edges)):
        name = edges["name"].iloc[i]
        movie = edges["movie"].iloc[i]
        table[int(name[2:])].append(int(movie[2:]))
    for key in list(table.keys()):
        table[key] = set(table[key])
    for i in range(len(people)):
        for j in range(i, len(people)):
            if have_intersection(table[people[i]], table[people[j]]):
                src.append(people[i])
                dest.append(people[j])
    pd.DataFrame(
            {"p1": src, "p2": dest})[["p1", "p2"]].to_csv(
                    "data/crew_network.txt", index = False)
        
generate_edges(names_df)
filter_edges()
