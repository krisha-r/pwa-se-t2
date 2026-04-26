from flask import Flask, render_template, request, redirect, session, flash
import db
from flask_bcrypt import Bcrypt

#Activate Flask app
app = Flask(__name__)
#Create app secret key
app.secret_key = "lca"
bcrypt = Bcrypt(app)


#Create home page for PWA
@app.route("/")
def Home():
    #Create blank username and guess data
    username = ''
    ReviewData = ""
    #Check if the user is logged in
    if session.get('username'):
        #If ther user is logged in then title case their username
        username = session['username'].title()
        #Fetch all guesses from the guesses database using GetAllReviews function from db.py
        ReviewData = db.GetAllReviews()
    #Render the index.html page, and send through the parameters ReviewData and username
    #The Reviewdata will display the table
    #The username, if logged in, will display the username on the home page
    return render_template("index.html", reviews=ReviewData, name=username)

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

#Create the add view page for the PWA, the get request will retrieve the data(add review data) and the post request will send through the review details
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
        movie_show = request.form['movie_show']
        format = request.form['format']
        rating = request.form['rating']
        review = request.form['review']
        # Add the data to the review database using the AddReview function from db.py
        db.AddReview(user_id, movie_show, format, rating, review)
        return redirect("/")
    #Render the template add.html
    return render_template("add.html")

#Create the edit review webpage for the PWA. The get request will retrieve the data(review data) and the post request will send through the new review data
@app.route("/edit", methods=["GET", "POST"])
def Edit():
    #if the user is not signed in, then the user will be directed back to the home page
    if session.get('username') == None:
        return redirect("/")    
    
    #Checks if the user submitted the form
    if request.method == 'POST':
        #If the user has submitted the form
        #Collect the review id from the form
        query = int(request.form['id'])
        #Collect the user id
        user_id = session['id']
        #Collect the movie and review details
        movie_show = request.form['movie_show']
        format = request.form['format']
        rating = request.form['rating']
        review = request.form['review']
        # Update the review data using the UpdateReview function from db.py
        db.UpdateReview(user_id, movie_show, format, rating, review, id=query)
        #Redirect user back to home page
        return redirect("/")
    else:
        #If the user hasn't submitted the form yet
        #Collect the review id from the url
        raw_query = request.args.get('q')
        try:
            # Try and convert the query into a integer
            query = int(raw_query)
            #Get the corresponding review from the database using the GetOneReview function from db.py
            review = db.GetOneReview(id=query)
            #If the user id from the review and the session user id don't match then redirect the user back to home page
            if review['user_id'] != session['id']:
                return redirect("/")
        except:
            # If an error is detected when trying to convert the query into an integer; e.g. the url doesn't collect a integer
            # Then redirect user to home page
            return redirect("/")
    # Render the edit.html template and push through the review data into the html page
    return render_template("edit.html", review=review)
      
# Create the delete review webpage to allow users to delete their reviews
@app.route("/delete")
def Delete():
    # If the user is not logged in then redirect them back to the home page
    if session.get('username') == None:
        return redirect("/")
    #Get the reviwe number from the url
    raw_query = request.args.get('q')
    try:
        # Try and convert the review number into an integer
        query = int(raw_query)
        # Get the corresponding review from the database by using the function from db.py
        review = db.GetOneReview(id=query)
        # If the user id from the review and the session id don't match then redirect user to home page
        if review['user_id'] != session['id']:
            return redirect("/")
        # Using the DeleteReview function from the db.py, pass through the id parameter and delete the entry
        db.DeleteReview(id=query)
    except Exception as e:
        # If an error is caught, e.g. trying to convert the query into an integer then redirect user back to home page
        return redirect("/")
    # If the review is deleted then redirect user back to home page
    return redirect("/")
    


# if the is being run by python then the __name__ become __main__
if __name__ == "__main__":
    #If the file is run through python then run the Flask app on the port 5000 on the local host
    #Debug mode is off
    app.run(debug=False, port=5000)