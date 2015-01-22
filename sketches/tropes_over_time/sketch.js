d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

$(function() {

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  var chart = d3.select('.viz');
  var svg = chart.append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var decades = [
        'Films of the 1920s', 'Films of the 1930s', 'Films of the 1940s',
        'Films of the 1950s', 'Films of the 1960s', 'Films of the 1970s',
        'Films of the 1980s', 'Films of the 1990s', 'Films of the 2000s',
        'Films of the 2010s'
    ];
  var x = d3.scale.ordinal()
    .rangeBands([0, width])
    .domain(decades);

  var y = d3.scale.linear()
    .range([height, 0]);

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient('left');

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient('bottom');

  var total_counts = [];
  var line = d3.svg.line()
    .interpolate("cardinal")
    .x(function(d, i) { return x(d[0]); })
    .y(function(d, i) { return y(d[1] / total_counts[i][1]); });

  d3.json('../../data/results/male_film_tropes.json', function(data) {

    // get aggregate time period counts

    decades.forEach(function(decade, idx) {
      total_counts.push([decade, 0]);
    });

    data.values.forEach(function(d) {
      d[1].decade_counts.forEach(function(m, i) {
        total_counts[i][1] += m[1];
      });
    });

    var min = 0;
    var max = data.values.reduce(function(prev, current, index, array) {
      var y = d3.max(current[1].decade_counts, function(m, idx) {
        return m[1] / total_counts[idx][1];
      });
      var x = d3.max([prev, y]);
      return x;
    }, 0);

    y.domain([min, max]);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("decade");

    var path_selected = svg.append("g");
    var paths_g = svg.append("g");

    var binding = paths_g.selectAll("path")
      .data(data.values, function(d) {
        return d[0];
      });

    var paths = binding.enter()
      .append("path")
      .attr("transform", "translate("+ x.rangeBand()/2 +","+ 0 +")")
      .classed("trope", true)
      .attr("data-trope", function(d) { return d[0]; })
      .datum(function(d) {
        return d[1].decade_counts;
      })
      .attr("d", line);

    // list
    var listbinding = d3.select(".list")
      .selectAll("li")
      .data(data.values, function(d) {
        return d[0];
      });

    var currentlySelected;
    listbinding.enter()
      .append("li")
      .attr("data-trope", function(d) { return d[0]; })
      .text(function(d) { return d[0]; })
      .on("mouseover", function(d) {
        if (currentlySelected) currentlySelected.classed("selected", false);
        var p = svg.select("path[data-trope=" + d[0] +"]")
          .classed("selected", true)
          .moveToFront();
        currentlySelected = p;
      });

  });

});