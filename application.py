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
    conn = sqlite3.connect('football.db')
    c = conn.cursor()

    c.execute("""select weekNumber from currentWeek""")
    currentWeek = c.fetchone()[0]

    #################### week 1 hard coded in ################################
    c.execute("""select playerID from fantasyPlayerGame
                where week = '1'""")
    players = c.fetchall()

    playerList = []
    for player in players:
        playerList.append(player[0])

    print(playerList)
    print(currentWeek)

    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    ####################### week one hard coded in ############################
    #if (1==0):
    c.execute("""select playerid, name, week,
         PassingYards, PassingTouchdowns, PassingInterceptions, RushingYards, RushingTouchdowns, Receptions, ReceivingYards, ReceivingTouchdowns, TwoPointConversionPasses, TwoPointConversionRuns,
         TwoPointConversionReceptions, FumblesLost, FumbleReturnTouchdowns, ExtraPointsMade, FieldGoalsMade0to19, FieldGoalsMade20to29, FieldGoalsMade30to39, FieldGoalsMade40to49, FieldGoalsMade50Plus
         from playerGame2019
         where seasonType = '1'
         and week = '1'
         and playerid in (?, ?, ?, ?, ?)""", (playerList[0], playerList[1], playerList[2], playerList[3], playerList[4]))

    playerGame = c.fetchall()
    #print(playerGame)
    for pg in playerGame:
        print(f"{pg['playerID']}")
    #print(playerList)
    print(currentWeek)

    return render_template("season.html", players = players, playerGame = playerGame, currentWeek=currentWeek)
    #else:
        #return render_template("season.html")



@app.route("/startOver")
def startOver():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("""update currentWeek set weekNumber = 1""")
    c.execute("""delete from fantasyTeam""")
    conn.commit()
    return render_template("season.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/playNextWeeksGame")
def playNextWeeksGame():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()

    c.execute("""select weekNumber from currentWeek""")
    currentWeek = c.fetchone()[0]

    c.execute("""update currentWeek set weekNumber = weekNumber + 1""")
    conn.commit()

    c.execute("""select playerID from fantasyTeam""")
    players = c.fetchall()

    playerList = []
    for player in players:
        playerList.append(player[0])

    for player in playerList:
        c.execute("""INSERT INTO FantasyPlayerGame (playerId, week)
                    VALUES (?, ?)"""
                    , (player, currentWeek))
        conn.commit()

    return render_template("season.html")

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

