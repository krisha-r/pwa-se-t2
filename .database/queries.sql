-- CREATE TABLE Guesses (id INTEGER PRIMARY KEY AUTOINCREMENT,
--                       user_id INTEGER,
--                       date TEXT NOT NULL,
--                       score INTEGER,
--                       game TEXT NOT NULL);

-- 
-- CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT,
--                     username TEXT UNIQUE NOT NULL,
--                     password NOT NULL);


CREATE TABLE Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT NOT NULL,
                    movie_show TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    review TEXT);
