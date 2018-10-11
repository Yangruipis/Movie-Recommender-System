df <- read.csv("ml-20m/movies.csv")
index <- 0
df[["movie_year"]] <- mapply(
    as.vector(df[["title"]]), FUN = function(x) {
        items <- unlist(strsplit(trimws(x), split = "\\(|\\)"))
        a <- as.integer(items[length(items)])
        index <<- index + 1
        if(is.na(a)){
            print(index)
            print(x)
        } else {
            a
        }
    })
