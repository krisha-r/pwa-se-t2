from flask import Flask, render_template, request
import db

app = Flask(__name__)
app.secret_key = "gtg"

@app.route("/")
def Home():
    guessData = db.GetAllGuesses() # Note: the new line
    return render_template("index.html", guesses=guessData)

app.run(debug=True, port=5000)