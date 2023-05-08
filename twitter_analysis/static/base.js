$(document).ready(function () {
  var elements = document.getElementsByClassName("dropdown-item");
  let graph_data;
  fetch("/getChartData")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      graph_data = data;
      $("#reload").css("display", "none");
      $("#main-container").css("display", "block");
    });
  function create_line_chart(x, y, topic, tweets, summaries) {
    $("#analysis").append(
      '<h1 id = "title" style="margin-top: 20px;text-align: left;margin-left: 25px;margin-bottom: 60px;">' +
        topic +
        "</h1>"
    );
    $("#analysis").append(
      '<canvas id="myChart" style="position: relative; height:60vh; width:80vw"></canvas>'
    );
    let dataset = [
      {
        label: "Negative",
        data: y["Negative"],
        borderColor: "#9BD0F5",
        backgroundColor: "#9BD0F5",
        fill: false,
        yAxisID: "y",
      },
      {
        label: "Neutral",
        data: y["Neutral"],
        borderColor: "#FFB1C1",
        backgroundColor: "#FFB1C1",
        fill: false,
        yAxisID: "y",
      },
      {
        label: "Positive",
        data: y["Positive"],
        borderColor: "#4BC0C0",
        backgroundColor: "#4BC0C0",
        fill: false,
        yAxisID: "y",
      },
    ];

    new Chart("myChart", {
      type: "line",
      data: { labels: x, datasets: dataset },
      options: {
        plugins: {
          legend: {
            position: "top",
            align: "start",
          },
          tooltip: {
            external: function (context) {
              // Tooltip Element
              let tooltipEl = document.getElementById("chartjs-tooltip");

              // Create element on first render
              if (!tooltipEl) {
                tooltipEl = document.createElement("div");
                tooltipEl.id = "chartjs-tooltip";
                tooltipEl.innerHTML = "<table></table>";
                document.body.appendChild(tooltipEl);
              }
              let summary = document.getElementById("daily-summary");
              if (!summary) {
                summary = document.createElement("div");
                summary.id = "daily-summary";
                summary.innerHTML =
                  '<h2>SUMMARY (via CHATGPT)</h2><div style="border:1px solid black";></div>';
                document.body.appendChild(summary);
              }
              // Hide if no tooltip
              const tooltipModel = context.tooltip;
              if (tooltipModel.opacity === 0) {
                tooltipEl.style.opacity = 0;
                return;
              }

              // Set caret Position
              tooltipEl.classList.remove("above", "below", "no-transform");
              if (tooltipModel.yAlign) {
                tooltipEl.classList.add(tooltipModel.yAlign);
              } else {
                tooltipEl.classList.add("no-transform");
              }

              // Set Text
              if (tooltipModel.body) {
                let items = tweets[x.indexOf(context.tooltip.title[0])];
                let innerHtml = "<thead>";
                innerHtml += "<tr><th>" + "TOP TWEETS" + "</th></tr>";

                innerHtml += "</thead><tbody>";

                // items[0].forEach(function(body, i) {
                //     const colors = tooltipModel.labelColors[i];
                //     let style = '; border-color:' + colors.borderColor;
                //     style += '; border-width: 2px';
                //     style += '; font-size: 12px';
                //     const span = '<span style="' + style + '">'+(i+1)+'.) ' + body + '</span>';
                //     innerHtml += '<tr><td>' + span + '</td></tr><br>';
                // });
                // let iframeLink = "https://twitter.com/Interior/status/1650649875049074688";
                let iframeLink =
                  "https://twitter.com/Interior/status/" + items[0][0];
                let link =
                  `https://twitframe.com/show?url=` +
                  encodeURIComponent(iframeLink);
                innerHtml += `<iframe border=0 frameborder=0 height=500px width=100% src=${link}></iframe>`;
                innerHtml += "</tbody>";

                let tableRoot = tooltipEl.querySelector("table");
                tableRoot.innerHTML = innerHtml;
              }
              let summ = summaries[x.indexOf(context.tooltip.title[0])];
              let summaryHtml = "<p>";
              summaryHtml += summ;
              summaryHtml += "</p>";
              let summaryRoot = summary.querySelector("div");
              summaryRoot.innerHTML = summaryHtml;

              summary.style.position = "absolute";
              summary.style.right = "1px";
              summary.style.top = "1px";
              summary.style.fontSize = "10px";
              summary.style.height = "40px";
              summary.style.width = "700px";
              summary.style.pointerEvents = "none";

              // Display, position, and set styles for font
              tooltipEl.style.opacity = 1;
              tooltipEl.style.position = "absolute";
              tooltipEl.style.top = "250px";
              tooltipEl.style.left = "150px";
              tooltipEl.style.height = "100px";
              tooltipEl.style.width = "500px";
              tooltipEl.style.padding =
                tooltipModel.padding + "px " + tooltipModel.padding + "px";
              tooltipEl.style.pointerEvents = "none";
            },
          },
        },
        
        responsive: true,
        interaction: {
          mode: "index",
          intersect: false,
        },
        stacked: false,
        scales: {
          yAxes: [
            {
              type: "linear",
              display: true,
              position: "left",
              id: "y",
            },
          ],
        },
      },
    });
  }

  function create_bar_chart(x, y) {
    $("#analysis").append(
      '<canvas id="myChart1" style="position: relative; height:60vh; width:80vw"></canvas>'
    );
    let dataset = [
      {
        label: "Negative",
        data: y["Negative"],
        backgroundColor: "#9BD0F5",
        stack: "Stack 0",
      },
      {
        label: "Neutral",
        data: y["Neutral"],
        backgroundColor: "#FFB1C1",
        stack: "Stack 1",
      },
      {
        label: "Positive",
        data: y["Positive"],
        backgroundColor: "#4BC0C0",
        stack: "Stack 2",
      },
    ];
    new Chart("myChart1", {
      type: "bar",
      data: { labels: x, datasets: dataset },
      options: {
        responsive: true,
        scales: {
          y: {
            stacked: true,
          },
        },
        legend: { display: false },
        title: {
          display: true,
          text: event.target.innerText,
        },
      },
    });
  }

  function create_pie_chart(y) {
    $("#analysis").append(
      '<canvas id="myChart2" style="position: relative;margin-left: 480; height:500px !important; width:500px !important"></canvas>'
    );
    let data = {
      labels: ["Negative", "Positive", "Neutral"],
      datasets: [
        {
          data: [
            y["Negative"].reduce((a, b) => a + b, 0),
            y["Positive"].reduce((a, b) => a + b, 0),
            y["Neutral"].reduce((a, b) => a + b, 0),
          ],
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)",
          ],
          hoverOffset: 4,
        },
      ],
    };
    new Chart("myChart2", {
      type: "doughnut",
      data: data,
      options: {
        responsive: false,
        aspectRatio: 3.0,
      },
    });
  }
  Array.from(elements).forEach((element) => {
    element.addEventListener("click", (event) => {
      $("#title").remove();
      $("#myChart").remove();
      $("#myChart1").remove();
      $("#myChart2").remove();
      let x = graph_data[event.target.innerText]["X_data"];
      let y = graph_data[event.target.innerText]["Y_data"];
      let tweets = graph_data[event.target.innerText]["Top Tweets"];
      let summaries = graph_data[event.target.innerText]["Summary"];
      create_line_chart(x, y, event.target.innerText, tweets, summaries);
      create_bar_chart(x, y);
      create_pie_chart(y);
    });
    $("#analysis").css("display", "block");
  });
});
