function BuildChart(labels, values, legend, position) {
    var ctx = document.getElementById(position).getContext('2d');
    
    var chartData = {
        labels: labels,
        datasets: [{
            label: legend, // Name the series
            data: values, // Specify the data values array
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            spanGaps: false
        }]};

    var options = {
      responsive: false, // Instruct chart js to respond nicely.
      maintainAspectRatio: true, // Add to prevent default behaviour of full-width/height 
    };
    
    var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: options
    });

    return myChart;
}

// https://css-tricks.com/the-many-ways-of-getting-data-into-charts/

/*
var chartData = {
    labels : [{% for item in labels %}"{{item}}",{% endfor %}],
    datasets : [{
    label: '{{ legend }}',
    fill: true,
    lineTension: 0.1,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "rgba(75,192,192,1)",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBorderColor: "rgba(75,192,192,1)",
    pointBackgroundColor: "#fff",
    pointBorderWidth: 1,
    pointHoverRadius: 5,
    pointHoverBackgroundColor: "rgba(75,192,192,1)",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    pointHoverBorderWidth: 2,
    pointRadius: 1,
    pointHitRadius: 10,
    data : [{% for item in values %}
              {{item}},
            {% endfor %}],
    spanGaps: false
}]
};
*/