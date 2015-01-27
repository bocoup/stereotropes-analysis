// move a node up to be in the front...
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

var decades = [
  'Films of the 1920s', 'Films of the 1930s', 'Films of the 1940s',
  'Films of the 1950s', 'Films of the 1960s', 'Films of the 1970s',
  'Films of the 1980s', 'Films of the 1990s', 'Films of the 2000s',
  'Films of the 2010s'
];

d3.chart("LineGraph", {

  initialize: function(options) {

    this.format(options.format || 'total');
    this.total_counts = []; // total counts by decade

    this.margin = {
      top: 20, right: 20, bottom: 30, left: 50
    };
    this.width(options.width - this.margin.left - this.margin.right);
    this.height(options.height - this.margin.top - this.margin.bottom);

    var svg = this.base.append("svg")
      .attr("width", this.width() + this.margin.left + this.margin.right)
      .attr("height", this.height() + this.margin.top + this.margin.bottom);

    this.bases = {
      axes: {
        x : svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + this.height() + ")"),

        y : svg.append("g")
          .attr("class", "y axis")
      },

      paths: svg.append("g")
        .attr("class", "paths")
    };

    this.scales = {
      x : d3.scale.ordinal()
        .rangeBands([0, this.width()])
        .domain(decades),
      y : d3.scale.linear()
      .range([this.height(), 0])
    };

    this.axes = {
      x : d3.svg.axis()
        .scale(this.scales.x)
        .orient('bottom')
        .tickFormat(function(d) {
          return d.substring(13,19);
        }),
      y : d3.svg.axis()
        .scale(this.scales.y)
        .orient('left')
    };

    var chart = this;
    this.line = d3.svg.line()
      // .interpolate("cardinal")
      .x(function(d, i) { return chart.scales.x(d[0]); })
      .y(function(d, idx) {

        if (chart.format() === 'total') return chart.scales.y(d[1]);
        if (chart.format() === 'decade') {
          return chart.scales.y(d[1] / chart.total_counts[idx][1]);
        }
        if (chart.format() === 'trope') return chart.scales.y(d[1] / chart.total_counts[d[2]]);

        return chart.scales.y(d[1]);
      });

    // render x axis (it will never change)
    this.bases.axes.x.call(this.axes.x);

    this.layer('paths', this.bases.paths, {
      dataBind: function(data) {
        return this.selectAll('path')
          .data(data, function(d) {
            return d.name;
          });
      },
      insert: function() {
        var chart = this.chart();
        return this.append("path")
          .classed("trope", true)
          .attr("transform", "translate("+ chart.scales.x.rangeBand()/2 +","+ 0 +")");
      },
      events: {
        "enter": function() {
          var chart = this.chart();
          this.attr("trope", function(d) {
            return d.name;
          }).datum(function(d) {
            return d.decade_counts;
          }).attr("d", chart.line);
        },
        "update": function() {
          this.datum(function(d) {
            return d.decade_counts;
          }).attr("d", chart.line);
        },
        "exit:transition": function() {
          this.attr('opacity', 0).remove();
        }
      }

    });
  },

  // Displaying values. Options are:
  // total - raw counts
  // decade - this tropes utilization over that decade across all tropes
  // trope - this tropes utilization in that decade over time
  format: function(name) {
    if (arguments.length) {
      this._format = name;
      return this;
    } else {
      return this._format;
    }
  },

  highlight: function(name) {
    if (this._currentlySelected) {
      this._currentlySelected.classed("selected", false);
    }
    var p = this.bases.paths.select("path[trope=" + name +"]")
      .classed("selected", true)
      .moveToFront();

    this._currentlySelected = p;
    return this;
  },

  transform: function(data) {
    var chart = this;
    var min = 0;

    // aggregate by decade [[decade, totalForDecade], ...]
    if (this.format() === 'decade') {
      chart.total_counts = [];
      decades.forEach(function(decade) {
        chart.total_counts.push([decade, 0]);
      });

      data.forEach(function(d) {
        d.decade_counts.forEach(function(m, i) {
          chart.total_counts[i][1] += m[1];
        });
      });
    }

    // aggregate by trope
    if (this.format() === 'trope') {
      chart.total_counts = {};
      data.forEach(function(d) {
        if (chart.total_counts[d.name]) {
          chart.total_counts[d.name] += d.films_count;
        } else {
          chart.total_counts[d.name] = d.films_count;
        }
      });
    }

    var max = data.reduce(function(prev, current, index, array) {
      var trope = current.name;
      var y = d3.max(current.decade_counts, function(m, idx) {
        if (chart.format() === 'total') {
          return m[1];
        }
        if (chart.format() === 'decade') {
          return m[1] / chart.total_counts[idx][1];
        }
        if (chart.format() === 'trope') {
          return m[1] / chart.total_counts[trope];
        }
      });
      var x = d3.max([prev, y]);
      return x;
    }, 0);

    console.log(min, max);
    this.scales.y.domain([min,max]);

    // update y axis. X is fixed, because all decades.
    this.bases.axes.y.call(this.axes.y);

    return data;

  },

  width: function(width) {
    if (arguments.length) {
      this._width = width;
      return this;
    } else {
      return this._width;
    }
  },

  height: function(height) {
    if (arguments.length) {
      this._height = height;
      return this;
    } else {
      return this._height;
    }
  }

});
