from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from random import randint, shuffle

app = Flask(__name__, template_folder="Templates")
app.secret_key = "notationmate"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

File = ["a","b","c","d","e","f","g","h"]
Rank = ["1","2","3","4","5","6","7","8"]

def generatePos():
    randomFile = randint(0,7)
    randomRank = randint(0,7)
    selectedFile = File[randomFile]
    selectedRank = Rank[randomRank]
    return selectedFile + selectedRank

def createArray():
    squares = []
    squares.append(generatePos())
    while len(squares) < 4:
        randomSquare = generatePos()
        if randomSquare not in squares:
            squares.append(randomSquare)
    return squares

@app.route("/", methods=["POST","GET"])
def default():
    if request.method == "POST":
        return redirect(url_for("play"))
    else:
        return render_template("home.html")

@app.route("/play/", methods=["POST","GET"])
def play():
    if request.method == "POST":
        if request.form["submit"] == session["answer"]:
            session["right"] += 1
        else:
            session["wrong"] += 1
        answerArray = createArray()
        session["answer"] = answerArray[0]
        shuffle(answerArray)
        return render_template("play.html", square=session["answer"], choices=answerArray, right=session["right"],wrong=session["wrong"])
    else:
        session["right"] = 0
        session["wrong"] = 0
        answerArray = createArray()
        session["answer"] = answerArray[0]
        shuffle(answerArray)
        return render_template("play.html", square=session["answer"], choices=answerArray,right=0,wrong=0)


if __name__ == "__main__":
    app.run(debug=True, port=1234)
