$(document).ready(function () {
  var elements = document.getElementsByClassName("dropdown-item");
  let graph_data;
  fetch('/getChartData')
  .then((response)=>{
    return response.json()
  })
  .then((data)=>{
    graph_data = data;
    $('#reload').css("display","none");
    $('#main-container').css("display","block")
  })
  function create_line_chart(x, y, topic) {
    $("#analysis").append(
      '<h1 id = "title" style="text-align: center">'+topic+'</h1>'
      
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
      let x = graph_data[event.target.innerText]['X_data']
      let y = graph_data[event.target.innerText]['Y_data']
      create_line_chart(x, y,event.target.innerText);
      create_bar_chart(x, y);
      create_pie_chart(y);
    });
    $("#analysis").css("display", "block");
  });
});
