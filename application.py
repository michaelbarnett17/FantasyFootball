from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/createTeam")
def createTeam():
    return render_template("createTeam.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/season")
def season():
    return render_template("season.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")