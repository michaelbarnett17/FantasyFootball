import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/playNextWeeksGame")
def playNextWeeksGame():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()

    c.execute("""select weekNumber from currentWeek""")
    currentWeek = c.fetchone()[0]

    if (int(currentWeek) <= 17):
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
    return season()

@app.route("/season")
def season():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("""select weekNumber from currentWeek""")
    currentWeek = int(c.fetchone()[0])

    conn.row_factory = sqlite3.Row

    fantasyGames = []
    pointsArray = []
    totalPoints = 0

    for week in range(1, currentWeek):
        #if (1==0):
        c = conn.cursor()
        c.execute("""select PG.playerid, name, PG.week,
                        PassingYards,
                        PassingTouchdowns,
                        PassingInterceptions,
                        RushingYards,
                        RushingTouchdowns,
                        Receptions,
                        ReceivingYards,
                        ReceivingTouchdowns,
                        TwoPointConversionPasses,
                        TwoPointConversionRuns,
                        TwoPointConversionReceptions,
                        FumblesLost,
                        FumbleReturnTouchdowns,
                        ExtraPointsMade,
                        FieldGoalsMade0to19,
                        FieldGoalsMade20to29,
                        FieldGoalsMade30to39,
                        FieldGoalsMade40to49,
                        FieldGoalsMade50Plus,

                        CAST(PassingYards AS decimal) / 25.0                AS PassingYards_Pts,
                        CAST(PassingTouchdowns AS decimal) * 4              AS PassingTouchdowns_Pts,
                        CAST(PassingInterceptions AS decimal) * -2          AS PassingInterceptions_Pts,
                        CAST(RushingYards AS decimal) / 10.0                AS RushingYards_Pts,
                        CAST(RushingTouchdowns AS decimal) * 6              AS RushingTouchdowns_Pts,
                        CAST(Receptions AS decimal) * 1                     AS Receptions_Pts,
                        CAST(ReceivingYards AS decimal) / 10.0              AS ReceivingYards_Pts,
                        CAST(ReceivingTouchdowns AS decimal) * 6            AS ReceivingTouchdowns_Pts,
                        CAST(TwoPointConversionPasses AS decimal) * 2
                        + CAST(TwoPointConversionRuns AS decimal) * 2
                        + CAST(TwoPointConversionReceptions AS decimal) * 2 AS TwoPointConversion_Pts,
                        CAST(FumblesLost AS decimal) * -2                   AS FumblesLost_Pts,
                        CAST(FumbleReturnTouchdowns AS decimal) * 6         AS FumbleReturnTouchdowns_Pts,
                        CAST(ExtraPointsMade AS decimal) * 1                AS ExtraPointsMade_Pts,
                        CAST(FieldGoalsMade0to19 AS decimal) * 3
                        + CAST(FieldGoalsMade20to29 AS decimal) * 3
                        + CAST(FieldGoalsMade30to39 AS decimal) * 3
                        + CAST(FieldGoalsMade40to49 AS decimal) * 3         AS FieldGoalsMade0to49_Pts,
                        CAST(FieldGoalsMade50Plus AS decimal) * 5           AS FieldGoalsMade50Plus_Pts,

                        + CAST(PassingYards AS decimal) / 25.0
                        + CAST(PassingTouchdowns AS decimal) * 4
                        + CAST(PassingInterceptions AS decimal) * -2
                        + CAST(RushingYards AS decimal) / 10.0
                        + CAST(RushingTouchdowns AS decimal) * 6
                        + CAST(Receptions AS decimal) * 1
                        + CAST(ReceivingYards AS decimal) / 10.0
                        + CAST(ReceivingTouchdowns AS decimal) * 6
                        + CAST(TwoPointConversionPasses AS decimal) * 2
                        + CAST(TwoPointConversionRuns AS decimal) * 2
                        + CAST(TwoPointConversionReceptions AS decimal) * 2
                        + CAST(FumblesLost AS decimal) * -2
                        + CAST(FumbleReturnTouchdowns AS decimal) * 6
                        + CAST(ExtraPointsMade AS decimal) * 1
                        + CAST(FieldGoalsMade0to19 AS decimal) * 3
                        + CAST(FieldGoalsMade20to29 AS decimal) * 3
                        + CAST(FieldGoalsMade30to39 AS decimal) * 3
                        + CAST(FieldGoalsMade40to49 AS decimal) * 3
                        + CAST(FieldGoalsMade50Plus AS decimal) * 5         AS PlayerPoints
                    from
                        playerGame2019 'PG'
                    join
                    fantasyplayergame 'FPG'
                    on PG.playerid = FPG.playerid and PG.week = FPG.week
                    where
                    seasonType = '1'
                    and PG.week = ?
                    order by PG.playerid""", (week,))

        fantasyGame = c.fetchall()
        #print(fantasyGame)

        gamePoints = 0
        for pg in fantasyGame:
            #print(f"{pg['PlayerPoints']}")
            pts = {pg['PlayerPoints']}.pop()
            gamePoints += pts

        totalPoints += gamePoints
        fantasyGames.append(fantasyGame)
        pointsArray.append(gamePoints)

    return render_template("season.html", pointsArray = pointsArray, fantasyGames = fantasyGames, totalPoints = totalPoints, currentWeek = currentWeek - 1)

@app.route("/eligiblePlayers")
def eligiblePlayers():
    conn = sqlite3.connect('football.db')
    c = conn.cursor()

    c.execute("""select playerid, firstName, lastName, position, team
                from player2019
                where team is not null
                and status = 'Active'
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

def getCurrentRoster(c, conn):
    c.execute("""select fantasyteam.playerid, firstName, lastName, position, WikipediaWordMarkUrl, photourl
                from player2019
                join fantasyteam
                on player2019.playerid = fantasyTeam.playerid
                join team2019
                on player2019.Team = Team2019.Key""")
    try:
        roster = c.fetchall()
        conn.close()
        return render_template("roster.html", roster = roster)
    except:
        conn.close()
        return render_template("roster.html", roster = roster)

@app.route("/startSeasonOver")
def startOver():
    totalPoints = 0
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("""update currentWeek set weekNumber = 1""")
    c.execute("""delete from FantasyPlayerGame""")
    conn.commit()
    return render_template("season.html", totalPoints = totalPoints)

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

# TODO: change "createTeam.html" to "index.html" when users can login
@app.route("/")
def index():
    return render_template("createTeam.html")

@app.route("/createTeam")
def createTeam():
    return render_template("createTeam.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

