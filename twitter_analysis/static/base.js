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
      // if (event.target.innerText == "Climate Change") {
      //   let x = graph_data['Climate Change']['X_data']

      //   let y = graph_data['Climate Change']['Y_data']

      //   create_line_chart(x, y,event.target.innerText);

      //   create_bar_chart(x, y);

      //   create_pie_chart(y);
      // } else if (event.target.innerText == "Russia Ukraine War") {
      //   let x = [
      //     "2023-01-27",
      //     "2023-01-28",
      //     "2023-01-29",
      //     "2023-01-30",
      //     "2023-01-31",
      //     "2023-02-01",
      //     "2023-02-02",
      //     "2023-02-03",
      //     "2023-02-04",
      //     "2023-02-05",
      //     "2023-02-06",
      //     "2023-02-07",
      //     "2023-02-08",
      //     "2023-02-09",
      //     "2023-02-10",
      //     "2023-02-11",
      //     "2023-02-19",
      //     "2023-02-20",
      //     "2023-02-21",
      //     "2023-02-22",
      //     "2023-02-23",
      //     "2023-02-24",
      //     "2023-02-25",
      //     "2023-02-26",
      //     "2023-02-27",
      //     "2023-02-28",
      //     "2023-03-01",
      //     "2023-03-02",
      //   ];
      //   let y = {
      //     Negative: [
      //       29.0, 29.0, 27.0, 48.0, 20.0, 33.0, 17.0, 353.0, 612.0, 2161.0,
      //       2767.0, 2075.0, 1499.0, 2898.0, 147.0, 271.0, 17.0, 49.0, 34.0,
      //       35.0, 23.0, 73.0, 39.0, 25.0, 291.0, 602.0, 5211.0, 220.0,
      //     ],
      //     Neutral: [
      //       23.0, 23.0, 19.0, 23.0, 12.0, 16.0, 15.0, 126.0, 205.0, 673.0,
      //       789.0, 652.0, 478.0, 784.0, 50.0, 93.0, 2.0, 57.0, 26.0, 20.0, 37.0,
      //       74.0, 36.0, 22.0, 93.0, 167.0, 1566.0, 55.0,
      //     ],
      //     Positive: [
      //       1.0, 3.0, 2.0, 1.0, 2.0, 0.0, 1.0, 13.0, 21.0, 78.0, 101.0, 114.0,
      //       104.0, 118.0, 7.0, 8.0, 1.0, 9.0, 2.0, 3.0, 5.0, 13.0, 3.0, 2.0,
      //       13.0, 22.0, 170.0, 9.0,
      //     ],
      //   };
      //   create_line_chart(x, y,event.target.innerText);

      //   create_bar_chart(x, y);

      //   create_pie_chart(y);
      // } else if (event.target.innerText == "Academic Workers Strike") {
      //   let x = [
      //     "2023-02-20",
      //     "2023-02-21",
      //     "2023-02-22",
      //     "2023-02-23",
      //     "2023-02-24",
      //     "2023-02-25",
      //     "2023-02-26",
      //     "2023-02-27",
      //     "2023-02-28",
      //     "2023-03-01",
      //   ];
      //   let y = {
      //     Negative: [
      //       2.0, 8.0, 2.0, 2.0, 8.0, 2.0, 5.0, 6.0, 12.0, 10.0, 4.0, 7.0, 4.0,
      //       3.0, 7.0, 15.0, 7.0,
      //     ],
      //     Neutral: [
      //       2.0, 4.0, 5.0, 2.0, 10.0, 10.0, 4.0, 9.0, 11.0, 14.0, 10.0, 11.0,
      //       4.0, 3.0, 7.0, 8.0, 9.0,
      //     ],
      //     Positive: [
      //       0.0, 3.0, 6.0, 0.0, 4.0, 4.0, 1.0, 3.0, 7.0, 5.0, 2.0, 3.0, 0.0,
      //       2.0, 3.0, 3.0, 1.0,
      //     ],
      //   };
      //   create_line_chart(x, y,event.target.innerText);

      //   create_bar_chart(x, y);

      //   create_pie_chart(y);
      // } else if (event.target.innerText == "Layoffs") {
      //   let x = [
      //     "2023-01-31",
      //     "2023-02-01",
      //     "2023-02-02",
      //     "2023-02-03",
      //     "2023-02-04",
      //     "2023-02-05",
      //     "2023-02-06",
      //     "2023-02-07",
      //     "2023-02-08",
      //     "2023-02-09",
      //     "2023-02-10",
      //     "2023-02-11",
      //     "2023-02-12",
      //     "2023-02-13",
      //     "2023-02-14",
      //     "2023-02-15",
      //     "2023-02-16",
      //     "2023-02-17",
      //     "2023-02-18",
      //     "2023-02-19",
      //     "2023-02-20",
      //     "2023-02-21",
      //     "2023-02-22",
      //     "2023-02-23",
      //     "2023-02-24",
      //     "2023-02-25",
      //     "2023-02-26",
      //     "2023-02-27",
      //     "2023-02-28",
      //     "2023-03-01",
      //     "2023-03-02",
      //     "2023-03-03",
      //     "2023-03-04",
      //   ];
      //   let y = {
      //     Negative: [
      //       19.0, 34.0, 47.0, 131.0, 76.0, 51.0, 144.0, 285.0, 359.0, 1348.0,
      //       284.0, 286.0, 34.0, 216.0, 13.0, 9.0, 8.0, 11.0, 8.0, 48.0, 123.0,
      //       119.0, 186.0, 293.0, 189.0, 126.0, 116.0, 263.0, 234.0, 2452.0,
      //       236.0, 91.0, 377.0,
      //     ],
      //     Neutral: [
      //       14.0, 33.0, 25.0, 76.0, 27.0, 27.0, 59.0, 93.0, 110.0, 432.0, 124.0,
      //       84.0, 13.0, 75.0, 3.0, 10.0, 7.0, 6.0, 6.0, 23.0, 44.0, 46.0, 71.0,
      //       119.0, 85.0, 42.0, 58.0, 106.0, 87.0, 785.0, 96.0, 24.0, 90.0,
      //     ],
      //     Positive: [
      //       2.0, 3.0, 7.0, 20.0, 9.0, 2.0, 18.0, 19.0, 30.0, 105.0, 24.0, 17.0,
      //       1.0, 27.0, 2.0, 3.0, 3.0, 0.0, 1.0, 8.0, 8.0, 15.0, 13.0, 35.0,
      //       19.0, 5.0, 11.0, 23.0, 22.0, 215.0, 20.0, 11.0, 32.0,
      //     ],
      //   };
      //   create_line_chart(x, y,event.target.innerText);

      //   create_bar_chart(x, y);

      //   create_pie_chart(y);
      // } else if (event.target.innerText == "Gun Violence") {
      //   let x = [
      //     "2023-01-31",
      //     "2023-02-01",
      //     "2023-02-02",
      //     "2023-02-03",
      //     "2023-02-04",
      //     "2023-02-05",
      //     "2023-02-06",
      //     "2023-02-07",
      //     "2023-02-08",
      //     "2023-02-09",
      //     "2023-02-10",
      //     "2023-02-11",
      //     "2023-02-12",
      //     "2023-02-13",
      //     "2023-02-18",
      //     "2023-02-19",
      //     "2023-02-20",
      //     "2023-02-21",
      //     "2023-02-22",
      //     "2023-02-23",
      //     "2023-02-24",
      //     "2023-02-25",
      //     "2023-02-26",
      //     "2023-02-27",
      //     "2023-02-28",
      //     "2023-03-01",
      //     "2023-03-02",
      //     "2023-03-03",
      //     "2023-03-04",
      //   ];
      //   let y = {
      //     Negative: [
      //       109.0, 136.0, 159.0, 181.0, 128.0, 95.0, 106.0, 98.0, 219.0, 956.0,
      //       220.0, 232.0, 86.0, 174.0, 11.0, 93.0, 155.0, 163.0, 162.0, 390.0,
      //       251.0, 101.0, 110.0, 125.0, 870.0, 2475.0, 250.0, 158.0, 445.0,
      //     ],
      //     Positive: [
      //       6.0, 15.0, 5.0, 3.0, 4.0, 0.0, 4.0, 3.0, 7.0, 46.0, 9.0, 6.0, 0.0,
      //       4.0, 0.0, 1.0, 3.0, 4.0, 5.0, 10.0, 3.0, 2.0, 4.0, 2.0, 15.0, 91.0,
      //       4.0, 8.0, 10.0,
      //     ],
      //     Neutral: [
      //       34.0, 28.0, 38.0, 36.0, 22.0, 7.0, 16.0, 26.0, 38.0, 225.0, 45.0,
      //       22.0, 13.0, 39.0, 1.0, 26.0, 26.0, 31.0, 19.0, 47.0, 23.0, 10.0,
      //       10.0, 18.0, 115.0, 542.0, 31.0, 19.0, 77.0,
      //     ],
      //   };
      //   create_line_chart(x, y,event.target.innerText);

      //   create_bar_chart(x, y);

      //   create_pie_chart(y);
      // }
    });
    $("#analysis").css("display", "block");
  });
});
