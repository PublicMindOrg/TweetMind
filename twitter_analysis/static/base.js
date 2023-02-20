$(document).ready(function () {
  var elements = document.getElementsByClassName("dropdown-item");

  Array.from(elements).forEach((element) => {
    element.addEventListener("click", (event) => {
      $("#myChart").remove();
      if (event.target.innerText == "Climate Change") {
        $("#analysis").append(
          '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>'
        );

        var xyValues = [
          { x: 50, y: 7 },
          { x: 60, y: 8 },
          { x: 70, y: 8 },
          { x: 80, y: 9 },
          { x: 90, y: 9 },
          { x: 100, y: 9 },
          { x: 110, y: 10 },
          { x: 120, y: 11 },
          { x: 130, y: 14 },
          { x: 140, y: 14 },
          { x: 150, y: 15 },
        ];

        new Chart("myChart", {
          type: "scatter",
          data: {
            datasets: [
              {
                pointRadius: 4,
                pointBackgroundColor: "rgb(0,0,255)",
                data: xyValues,
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: event.target.innerText,
            },
            legend: { display: false },
            scales: {
              xAxes: [{ ticks: { min: 40, max: 160 } }],
              yAxes: [{ ticks: { min: 6, max: 16 } }],
            },
          },
        });
      } else if (event.target.innerText == "Russia Ukraine War") {
        $("#analysis").append(
          '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>'
        );
        var xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
        var yValues = [55, 49, 44, 24, 15];
        var barColors = ["red", "green", "blue", "orange", "brown"];

        new Chart("myChart", {
          type: "bar",
          data: {
            labels: xValues,
            datasets: [
              {
                backgroundColor: barColors,
                data: yValues,
              },
            ],
          },
          options: {
            legend: { display: false },
            title: {
              display: true,
              text: event.target.innerText,
            }
          },
        });
      } else if (event.target.innerText == "Academic Workers Strike") {
        $("#myChart").remove();
        $("#analysis").append(
          '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>'
        );
        var xValues = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150];
        var yValues = [7, 8, 8, 9, 9, 9, 10, 11, 14, 14, 15];

        new Chart("myChart", {
          type: "line",
          data: {
            labels: xValues,
            datasets: [
              {
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "rgba(0,0,255,0.1)",
                data: yValues,
              },
            ],
          },
          options: {
            legend: { display: false },
            scales: {
              yAxes: [{ ticks: { min: 6, max: 16 } }],
            },
            title: {
              display: true,
              text: event.target.innerText,
            }
          },
        });
      } else if (event.target.innerText == "Layoffs") {
        $("#analysis").append(
          '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>'
        );

        var xyValues = [
          { x: 50, y: 7 },
          { x: 60, y: 8 },
          { x: 70, y: 8 },
          { x: 80, y: 9 },
          { x: 90, y: 9 },
          { x: 100, y: 9 },
          { x: 110, y: 10 },
          { x: 120, y: 11 },
          { x: 130, y: 14 },
          { x: 140, y: 14 },
          { x: 150, y: 15 },
        ];

        new Chart("myChart", {
          type: "scatter",
          data: {
            datasets: [
              {
                pointRadius: 4,
                pointBackgroundColor: "rgb(0,0,255)",
                data: xyValues,
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: event.target.innerText,
            },
            legend: { display: false },
            scales: {
              xAxes: [{ ticks: { min: 40, max: 160 } }],
              yAxes: [{ ticks: { min: 6, max: 16 } }],
            },
          },
        });
      } else if (event.target.innerText == "Gun Violence") {
        $("#analysis").append(
          '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>'
        );

        $("#analysis").append(
          '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>'
        );
        var xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
        var yValues = [55, 49, 44, 24, 15];
        var barColors = ["red", "green", "blue", "orange", "brown"];

        new Chart("myChart", {
          type: "bar",
          data: {
            labels: xValues,
            datasets: [
              {
                backgroundColor: barColors,
                data: yValues,
              },
            ],
          },
          options: {
            legend: { display: false },
            title: {
              display: true,
              text: event.target.innerText,
            },
          },
        });
      }
    });
  });
  $("#analysis").css("display", "block");
});
