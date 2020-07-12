var weekCount = 1;
var totalPoints = 0;
var yearStarted = false;
var year;
const rowBreak1 = 7;
const rowBreak2 = 13;
const finalWeek = 16;

document.querySelector("#nextWeek").onclick = function () {
    processWeek();
};

document.querySelector("#confirmYear").onclick = function () {
    var year = document.getElementById("seasonYear").value;

    if (year == null || year == "" || isNaN(year) || year != 2019) {
        alert("Application currently works for 2019 season only");
        return;
    }
    setYear();
    document.querySelector("#nextWeek").disabled = false;
};

document.querySelector("#startOver").onclick = function () {
    weekCount = 1;
    totalPoints = 0;
    yearStarted = false;
    row1 = document.querySelector("#week1-6");
    row2 = document.querySelector("#week7-12");
    row3 = document.querySelector("#week12-16");
    row1.innerHTML = "";
    row2.innerHTML = "";
    row3.innerHTML = "";
    document.getElementById("year").innerHTML ="";
    document.getElementById("week").innerHTML = "";;
    document.getElementById("points").innerHTML ="";
    document.getElementById("seasonYear").value ="";
    document.querySelector("#nextWeek").disabled = true;
};

function processWeek() {
    if (weekCount <= 16) {
        week = document.getElementById("week");
        week.innerHTML = weekCount;
        addWeek();
        weekCount++;
    } else {
        alert("Season Finished. Your overall point total is: ");
    }
}

function addWeek() {
    var row;

    if (weekCount < rowBreak1) {
        row = document.querySelector("#week1-6");
    } else if (weekCount < rowBreak2) {
        row = document.querySelector("#week7-12");
    } else if (weekCount <= finalWeek) {
        row = document.querySelector("#week12-16");
    } else {
        alert("Something went wrong");
        return;
    }

    var week = document.createElement("div");

    week.setAttribute("id", "week" + weekCount);
    week.setAttribute("class", "col-md-2");
    // TODO implement weekly points
    week.innerHTML = "Week " + weekCount + "<span id='spacer'></span>Points:";

    var htmlPlayer1 = document.createElement("div");
    var htmlPlayer2 = document.createElement("div");
    var htmlPlayer3 = document.createElement("div");

    htmlPlayer1.innerHTML = createHTML(1);
    htmlPlayer2.innerHTML = createHTML(2);
    htmlPlayer3.innerHTML = createHTML(3);

    week.appendChild(htmlPlayer1);
    week.appendChild(htmlPlayer2);
    week.appendChild(htmlPlayer3);
    row.appendChild(week);
}

function setYear() {
    if (yearStarted == false) {
        year = document.getElementById("seasonYear").value;
        var yearHtml = document.getElementById("year");
        yearHtml.innerHTML = year;
        yearStarted = true;
    }
    else
    {
      alert("Season already in Progress. Select \"Start Over\" to pick a new year.");
    }
}

function createHTML(playerNumber) {
  // playerNumber + weekCount is used to identify the button
  var html =

  '<button type="button" class="btn btn-dark" data-toggle="collapse" data-target="#' + playerNumber + weekCount + '">Player' + playerNumber + '</button>' +
  '<div id="' + playerNumber + weekCount + '" class="collapse">'
  +
  `
    <table class="table table-sm">
    <thead class="thead-secondary">
      <tr>
        <th scope="col">Stat</th>
        <th scope="col">Qty</th>
        <th scope="col">Points</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">Passing Yards</th>
        <td>1</td>
        <td>2</td>
      </tr>
      <tr>
        <th scope="row">Passing Touchdowns</th>
        <td>3</td>
        <td>4</td>
      </tr>
      <tr>
        <th scope="row">Passing Interceptions</th>
        <td>5</td>
        <td>6</td>
      </tr>
      <tr>
        <th scope="row">Rushing Yards</th>
        <td>7</td>
        <td>8</td>
      </tr>
      <tr>
        <th scope="row">Receiving Yards</th>
        <td>9</td>
        <td>10</td>
      </tr>
      <tr>
        <th scope="row">Receiving Touchdowns</th>
        <td>11</td>
        <td>12</td>
      </tr>
      <tr>
        <th scope="row">2-Point Conversions</th>
        <td>13</td>
        <td>14</td>
      </tr>
      <tr>
        <th scope="row">Fumbles Lost</th>
        <td>15</td>
        <td>16</td>
      </tr>
      <tr>
        <th scope="row">Fumble Recovered for a Touchdown</th>
        <td>17</td>
        <td>18</td>
      </tr>
    </tbody>
    </table>
  </div>
  `;
  return html;
}

