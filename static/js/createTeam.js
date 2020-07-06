var playerCount = 1;
const maxPlayers = 3;
var QB = false;
var RB = false;
var WR = false;

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

    if ((playerPosition == "Quarterback" && QB == false) ||
        (playerPosition == "Running Back" && RB == false) ||
        (playerPosition == "Wide Receiver" && WR == false)) {

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

    var team = document.createElement("h5");
    team.innerHTML = playerTeam;

    var position = document.createElement("h5");
    position.innerHTML = playerPosition;


    div.appendChild(name);
    div.appendChild(team);
    div.appendChild(position);
    players.appendChild(div);

    playerCount++;
}

function setGlobalVariables(playerPosition) {

    if (playerPosition == "Quarterback") {
        QB = true;
        document.querySelector("#quarterBack").disabled = true;
    } else if (playerPosition == "Running Back") {
        RB = true;
        document.querySelector("#runningBack").disabled = true;
    } else if (playerPosition == "Wide Receiver") {
        WR = true;
        document.querySelector("#wideReceiver").disabled = true;
    } else {
        alert("invalid position");
    }
}