import sqlite3

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/createTeam")
def createTeam():
    return render_template("createTeam.html")

# TODO: change "createTeam.html" to "index.html" when users can login
@app.route("/")
def index():
    return render_template("createTeam.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/season")
def season():
    return render_template("season.html")

@app.route("/roster")
def roster():
    return render_template("roster.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/addPlayer", methods=["GET", "POST"])
def addPlayer():

    firstName = request.args.get("firstName")
    lastName = request.args.get("lastName")
    team = request.args.get("team")
    position = request.args.get("position")

    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("""select playerid, position
                from Player2019
                where firstName = ? collate nocase
                and lastName = ? collate nocase
                and team =?
                and position = ?"""
                , (firstName, lastName, team, position))

    try:
        player = c.fetchall()[0]

        print(player)
        print(player[0])
        print(player[1])

        c.execute("""select count(position)
                    from player2019
                    join fantasyteam
                    on player2019.playerid = fantasyTeam.playerid
                    where position = ?"""
                    , (player[1],))

        exisitingCount = c.fetchone()[0]
        print("exisiting count for this pos is ", exisitingCount)

        if (exisitingCount == 0):
            c.execute("""insert into fantasyteam (playerid)
                        values (?)"""
                        , (player[0],))
            conn.commit()
            return render_template("roster.html", player = player)
        else:
            player = ('You already have a ' + player[1],)
            return render_template("createTeam.html", player = player)

    except:
        return render_template("createTeam.html", player = None)



