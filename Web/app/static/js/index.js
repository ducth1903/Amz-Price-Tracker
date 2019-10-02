$(document).ready(function() {
    $("#no-btn").click(function() {
        window.location.href = "http://127.0.0.1:5000/";
    });

    $("#yes-btn").click(function() {
        $("#div_not_found_product").css({'display': 'inline'});
    });

    // ============================= PRICE GRAPH =============================
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#price_graph")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        // translate this svg element to leave some margin
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // X scale and axis
    var x = d3.scaleLinear()
        .domain([0, 100])               // this is [min, max] of the data
        .range([0, width]);             // this is corresponding value in pixel

    // Y scale and axis
    var y = d3.scaleLinear()
        .domain([0, 100])               // this is [min, max] of the data
        .range([height, 0]);            // this is corresponding value in pixel

    svg.append('g').attr("transform", "translate(0,"+height+")").call(d3.axisBottom(x))
        .append('g').call(d3.axisLeft(y));
    
    // Create data
    var data = [ {x:10, y:20}, {x:40, y:90}, {x:80, y:50} ]
    svg
        .selectAll("whatever")
        .data(data)
        .enter()
        .append("circle")
            .attr("cx", function(d){ return x(d.x) })
            .attr("cy", function(d){ return y(d.y) })
            .attr("r", 7)

    // d3.select("#price_graph")
    //     .append("svg")
    //     .append("circle").attr("cx", 50).attr("cy", 50).attr("r", 40).style("fill", "purple");

});