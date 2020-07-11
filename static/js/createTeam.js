var playerCount = 1;
const maxPlayers = 3;
var QB = false;
var RB = false;
var WR = false;

document.querySelector("#searchPlayer").onclick = function() {
    searchPlayer();
};

document.querySelector("#addPlayer").onclick = function() {
    processPlayer();
};

document.getElementById("startOver").onclick = function() {
    playerCount = 1;
    QB = false;
    RB = false;
    WR = false;
    document.querySelector("#players").innerHTML ="";
    document.querySelector("#startSeason").disabled = true;
    document.querySelector("#quarterBack").disabled = false;
    document.querySelector("#runningBack").disabled = false;
    document.querySelector("#wideReceiver").disabled = false;
};

function searchPlayer() {

}

function processPlayer() {

    if (playerCount > maxPlayers){
        alert("Your team is full, ready to start the season!");
        return;
    }

    var playerName = document.getElementById("playerName").value;
    var playerTeam = document.getElementById("playerTeam").value;
    var playerPosition = document.getElementById("playerPosition").value;

    if (playerName == null || playerName == "") {
        alert("Enter player name before submiting");
        return;
    }

    if ((playerPosition == "QB" && QB == false) ||
        (playerPosition == "RB" && RB == false) ||
        (playerPosition == "WR" && WR == false)) {

        setGlobalVariables(playerPosition);
        addPlayer(playerName, playerTeam, playerPosition);

        if (playerCount > maxPlayers){
            document.querySelector("#startSeason").disabled = false;
        }
    } else {
        alert("You already have a " + playerPosition);
        return;
    }
}

function addPlayer(playerName, playerTeam, playerPosition) {

    var players = document.querySelector("#players");

    var div = document.createElement("div");
    div.setAttribute("id", playerCount);
    div.setAttribute("class", "player");

    var name = document.createElement("h5");
    name.innerHTML = playerName;

    var position = document.createElement("h5");
    position.innerHTML = lookupPosition(playerPosition);

    var team = document.createElement("h5");
    team.innerHTML = lookupTeam(playerTeam);

    div.appendChild(name);
    div.appendChild(team);
    div.appendChild(position);

    players.appendChild(div);

    playerCount++;
}

function setGlobalVariables(playerPosition) {

    if (playerPosition == "QB") {
        QB = true;
        document.querySelector("#quarterBack").disabled = true;
    } else if (playerPosition == "RB") {
        RB = true;
        document.querySelector("#runningBack").disabled = true;
    } else if (playerPosition == "WR") {
        WR = true;
        document.querySelector("#wideReceiver").disabled = true;
    } else {
        alert("invalid position");
    }
}

function lookupPosition(playerPosition)
{
    if (playerPosition == "QB") {
        return "Quarterback";
    } else if (playerPosition == "RB") {
        return "Running Back";
    } else if (playerPosition == "WR") {
        return "Wide Receiver";
    }

}

function lookupTeam(playerTeam)
{
    var teams = {
        "ARI" : "Arizona Cardinals",
        "ATL" : "Atlanta Falcons",
        "BAL" : "Baltimore Ravens",
        "BUF" : "Buffalo Bills",
        "CAR" : "Carolina Panthers",
        "CHI" : "Chicago Bears",
        "CIN" : "Cincinnati Bengals",
        "CLE" : "Cleveland Browns",
        "DAL" : "Dallas Cowboys",
        "DEN" : "Denver Broncos",
        "DET" : "Detroit Lions",
        "GB"  : "Green Bay Packers",
        "HOU" : "Houston Texans",
        "IND" : "Indianapolis Colts",
        "JAX" : "Jacksonville Jaguars",
        "KC"  : "Kansas City Chiefs",
        "LAC" : "Los Angeles Chargers",
        "LAR" : "Los Angeles Rams",
        "LV"  : "Las Vegas Raiders",
        "MIA" : "Miami Dolphins",
        "MIN" : "Minnesota Vikings",
        "NE"  : "New England Patriots",
        "NO"  : "New Orleans Saints",
        "NYG" : "New York Giants",
        "NYJ" : "New York Jets",
        "PHI" : "Philadelphia Eagles",
        "PHO" : "Pittsburgh Steelers",
        "PIT" : "San Francisco 49ers",
        "SEA" : "Seattle Seahawks",
        "TB"  : "Tampa Bay Buccaneers",
        "TEN" : "Tennessee Titans",
        "WAS" : "Washington Redskins"
    };

    return teams[playerTeam];
}




