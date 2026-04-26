import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from main import bcrypt


def GetDB():
    # Create a function to connect to the created database
    db = sqlite3.connect(".database/lca.db")
    #Allow the access of the rows in the database using their value
    db.row_factory = sqlite3.Row
    #Return the database
    return db

def GetAllReviews():
    # Run the GetDB() and connect to the database
    db = GetDB()
    #Fetch all the data from the guesses table
    #Join the reviews and user table using the user id
    #Title case the username, by making the first letter uppercase and the rest of the username lowercase
    #Order the data in descending order by date
    guesses = db.execute("""SELECT Reviews.id, Reviews.user_id, Reviews.movie_show, Reviews.format, Reviews.rating, Reviews.review, UPPER(SUBSTR(Users.username, 1, 1)) || LOWER(SUBSTR(Users.username, 2)) AS username
                            FROM Reviews JOIN Users ON Reviews.user_id = Users.id
                            ORDER BY rating DESC""").fetchall()
    #Close the connection to the database
    db.close()
    #Return the guesses
    return guesses

#Create a function to check if the user provided the right login details
def CheckLogin(username, password):
    # Run the GetDB() and connect to the database
    db = GetDB()
    # Check if the username provided by the user matches a username in the database and then fetch that row from the table
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()
    # Check if the above line returned a row from the table
    if user is not None:
        # If the user provided the right username, then check if the password is right
        # Hash the password provided and check if it matches the password in the database
        # Use flask bcrypt to hash the password for better security
        if bcrypt.check_password_hash(pw_hash=user['password'], password=password):
            # They got it right, return their details 
            #If the password matches then return the user details, including user id, username and password
            return user
    # If the username or password don't exist in the database then return nothing
    return None

#Create a function to register a new user into the PWA
def RegisterUser(username, password):
    # Check that the username and password are both provided by the user
    if username is None or password is None:
        #If one is not provided then return False
        return False
    # Run the GetDB() and connect to the database
    db = GetDB()
    #Hash the password provided by the user using flask bcrypt 
    hash = bcrypt.generate_password_hash(password=password)
    
    
    try:
        #Try and add the username and password into the database
        db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
        db.commit()
    #If the username already exists then the below error will pop up, because each username must be unique in the database
    except sqlite3.IntegrityError as e:
        #If this error pops up, then except the error
        # Then rollback the previous commit and undo all changes, to ensure that the database is not locked down due to the error
        db.rollback()
        #Return False; the username and password were not added into the database
        return False
    #Return true if this error is not picked up; the username and password were added into the database
    return True

#Create a function to add user reviews into the database
def AddReview(user_id, movie_show, format, rating, review):
    # Check and ensure that the none of the entries are empty
    if  movie_show is None or rating is None:
        return False
    # Run the GetDB() and connect to the database
    db = GetDB()
    
    #Add the user_id, movie_score, rating, review into the reviews database
    db.execute("INSERT INTO Reviews(user_id, movie_show, format, rating, review) VALUES (?, ?, ?, ?, ?)",
               (user_id, movie_show, format, rating, review))
    #Commit the changes to the database
    db.commit()
    
    #Return true signalling that the review added into the table
    return True

#Create a function to allow users to update their older reviews
def UpdateReview(user_id, movie_show, format, rating, review, id):
    # If the user has not provided the movie/show name and the rating then return back False
    if  movie_show is None or rating is None:
        return False
    # Run the GetDB() and connect to the database
    db = GetDB()
    #From the reviews table, update the user_id, movie_show, format, rating and review fields using the input provdied by the user in the form
    # Find the review with the same id as the one provided and then update the table
    db.execute("""UPDATE Reviews
               SET user_id=?, movie_show=?, format=?, rating=?, review=?
               WHERE Reviews.id = ?""",
              (user_id, movie_show, format, rating, review, id))
    # Commit the changes to the database
    db.commit()
    #Return true to indicate that the review was updated
    return True

# Create a function to get one review from the table using an id
def GetOneReview(id):
    # Run the GetDB() and connect to the database
    db = GetDB()
    # To the variable review, save the entry that is fetched from the reviews table using the id provided
    review = db.execute("SELECT * FROM Reviews WHERE id=?", (id,)).fetchone()
    #Close the database
    db.close()
    #Return the review back to the main PWA
    return review


#Create a function to delete a user review based on the id the user provides
def DeleteReview(id):
    # Run the GetDB() and connect to the database
    db = GetDB()
    #From the reviews table remove the row depending on the id number
    db.execute("""DELETE FROM Reviews
               WHERE Reviews.id = ?""", (id,))
    #Commit the changes to the database
    db.commit()
    #Return true indicating that the review was deleted
    return True

    
    
    