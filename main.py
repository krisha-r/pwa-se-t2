from flask import Flask, render_template, request, redirect, session, send_from_directory, flash
import db

#Activate Flask app
app = Flask(__name__)
#Create app secret key
app.secret_key = "gtg"


#Create home page for PWA
@app.route("/")
def Home():
    #Create blank username and guess data
    username = ''
    guessData = ""
    #Check if the user is logged in
    if session.get('username'):
        #If ther user is logged in then title case their username
        username = session['username'].title()
        #Fetch all guesses from the guesses database using GetAllGuesses function from db.py
        guessData = db.GetAllGuesses() # Note: the new line
    #Render the index.html page, and send through the parameters guessData and username
    #The guessdata will display the table
    #The username, if logged in, will display the username on the home page
    return render_template("index.html", guesses=guessData, name=username)

#Create the login page for the PWA, the get request will retrieve data(the login page) and the post request will send through the username and password
@app.route("/login", methods=["GET", "POST"])
def Login():
    #Check if the user is already logged in
    if session.get('username') != None:
        #If the user is already logged in then redirect them to the home page
        return redirect("/")
    #Check if the user had submitted the form
    if request.method == "POST":
        #Get the username and password the user submitted
        username = request.form['username']
        #Lowercase the username; the username in the database is stored in lowercase
        username = username.lower()
        password = request.form['password']

        # Check if the username and password are in the database; using the CheckLogin method from the db.py
        user = db.CheckLogin(username, password)
        #Check if the user is logged in
        if user:
            #Save their id; using the id in the database
            session['id'] = user['id']
            #Save their username to the session; will be used later to check if the user is logged in or not
            session['username'] = username

            # Redirect user to homepage if they are logged in
            return redirect("/")
        else:
            #If they are not logged in then flash the message
            flash("Your username or password was incorrect")
    #Render the login.html page
    return render_template("login.html")

#Create the logout page
@app.route("/logout")
def Logout():
    #Clear the session; will remove previously stored user id and username
    session.clear()
    #Redirect user to homepage
    return redirect("/")

#Create the registration page, the get request will retrieve the data(register page) and the post request will send through the username and password
@app.route("/register", methods=["GET", "POST"])
def Register():
    #If the user is already logged in then redriect them to the home page
    if session.get('username') != None:
        return redirect("/")
    #Check if the user has submitted the form
    if request.method == "POST":
        #Retrieve the username from the form
        username = request.form['username']
        #Lowercase the username, to store into the database in lowercase
        username = username.lower()
        #Retrieve the password
        password = request.form['password']

        #Add the username and password to the database
        if db.RegisterUser(username, password):
            # If the username and password are added then redirect them to the homepage
            return redirect("/")
        else:
            # If the username and password aren't added to the username, flash the message the username is already taken
            flash("This username is already taken")
            
    #Render the template register.html
    return render_template("register.html")

#Create the add guess page for the PWA, the get request will retrieve the data(add guess data) and the post request will send through the guess details
@app.route("/add", methods=["GET","POST"])
def Add():
    # Check if the user is logged in
    if session.get('username') == None:
        #If they aren't logged in, redirect them back to the homepage
        return redirect("/")

    # Check if the user submitted the form
    if request.method == "POST":
        #Collect the data the user submitted, including the user id from the session id, the date, the game name and the score
        user_id = session['id']
        date = request.form['date']
        game = request.form['game']
        score = request.form['score']
        # Add the data to the guesses database using the AddGuess function from db.py
        db.AddGuess(user_id, date, game, score)
    #Render the template add.html
    return render_template("add.html")

# if the is being run by python then the __name__ become __main__
if __name__ == "__main__":
    #If the file is run through python then run the Flask app on the port 5000 on the local host
    #Debug mode is off
    app.run(debug=False, port=5000)