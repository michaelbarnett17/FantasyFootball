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

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")


@app.route("/eligiblePlayers")
def eligiblePlayers():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()

    c.execute("""select playerid, firstName, lastName, position, team
                from player2019
                where team is not null
                and team != ''
                and position in ('QB', 'RB', 'WR', 'TE', 'K')
                order by position""")
    try:
        eligiblePlayers = c.fetchall()
        conn.close()
        return render_template("createTeam.html", eligiblePlayers = eligiblePlayers)
    except:
        conn.close()
        return render_template("createTeam.html", eligiblePlayers = eligiblePlayers)

@app.route("/release")
def release():
    playerId = request.args.get("release")
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("""delete from fantasyteam
                where playerid = ?"""
                , (playerId,))
    conn.commit()
    conn.close()
    return roster()

@app.route("/roster")
def roster():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    return getCurrentRoster(c, conn)

@app.route("/addPlayer", methods=["GET", "POST"])
def addPlayer():
    firstName = request.args.get("firstName").strip()
    lastName = request.args.get("lastName").strip()
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

    return tryToAddPlayerToRoster(c, conn)

@app.route("/addPlayerFromList", methods=["GET", "POST"])
def addPlayerFromList():
    playerId = request.args.get("playerId")

    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("""select playerid, position
                from Player2019
                where playerId = ?"""
                , (playerId,))

    return tryToAddPlayerToRoster(c, conn)

def getCurrentRoster(c, conn):
    c.execute("""select fantasyteam.playerid, firstName, lastName, position, team, photourl
                from player2019
                join fantasyteam
                on player2019.playerid = fantasyTeam.playerid""")
    try:
        roster = c.fetchall()
        conn.close()
        return render_template("roster.html", roster = roster)
    except:
        conn.close()
        return render_template("roster.html", roster = roster)

def tryToAddPlayerToRoster(c, conn):
    try:
        player = c.fetchall()[0]

        c.execute("""select count(position)
                    from player2019
                    join fantasyteam
                    on player2019.playerid = fantasyTeam.playerid
                    where position = ?"""
                    , (player[1],))

        exisitingCount = c.fetchone()[0]

        if (exisitingCount == 0):
            c.execute("""insert into fantasyteam (playerid)
                        values (?)"""
                        , (player[0],))
            conn.commit()
            return getCurrentRoster(c, conn)
        else:
            player = ('You already have a ' + player[1],)
            conn.close()
            return render_template("createTeam.html", player = player)
    except:
        conn.close()
        return render_template("createTeam.html", player = None)


