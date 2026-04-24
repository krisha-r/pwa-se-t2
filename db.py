import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def GetDB():
    # Create a function to connect to the created database
    db = sqlite3.connect(".database/gtg.db")
    #Allow the access of the rows in the database using their value
    db.row_factory = sqlite3.Row
    #Return the database
    return db

def GetAllGuesses():
    # Run the GetDB() and connect to the database
    db = GetDB()
    #Fetch all the data from the guesses table
    #Join the guesses and user table using the user id
    #Title case the username, by making the first letter uppercase and the rest of the username lowercase
    #Order the data in descending order by date
    guesses = db.execute("""SELECT Guesses.date, Guesses.game, Guesses.score, UPPER(SUBSTR(Users.username, 1, 1)) || LOWER(SUBSTR(Users.username, 2)) AS username
                            FROM Guesses JOIN Users ON Guesses.user_id = Users.id
                            ORDER BY date DESC""").fetchall()
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
        if check_password_hash(user['password'], password):
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
    #Hash the password provided by the user
    hash = generate_password_hash(password)
    
    
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

#Create a function to add user guesses into the database
def AddGuess(user_id, date, game, score):
    # Check and ensure that the none of the entries are empty
    if date is None or game is None or score is None:
        return False
    # Run the GetDB() and connect to the database
    db = GetDB()
    
    #Add the user_id, date, game and score into the guesses database
    db.execute("INSERT INTO Guesses(user_id, date, game, score) VALUES (?, ?, ?, ?)",
               (user_id, date, game, score,))
    #Commit the changes to the database
    db.commit()
    
    #Return true signalling that the guess added into the table
    return True