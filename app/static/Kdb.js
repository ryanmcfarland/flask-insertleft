function connect(host, port){
    if ("WebSocket" in window) {
        //console.log("ws://"+host+":"+port);
        ws = new WebSocket("ws://"+host+":"+port);
    
        ws.onmessage = function(msg){
            var d = JSON.parse(msg.data);
            BuildChart(d.labels, d.values, "Monthly Data", "myChart2");
        };
    } else alert("WebSockets not supported on your browser.");
};

function sendMessage(){
    ws.send("grab")
};

// https://www.codewall.co.uk/chartjs-tutorial-for-beginners-with-pdf-1/
// https://css-tricks.com/the-many-ways-of-getting-data-into-charts/
