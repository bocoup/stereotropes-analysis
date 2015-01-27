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
      top: 50, right: 20, bottom: 30, left: 50
    };
    this.width(options.width - this.margin.left - this.margin.right);
    this.height(options.height - this.margin.top - this.margin.bottom);

    var svg = this.base.append("svg")
      .attr("width", this.width() + this.margin.left + this.margin.right)
      .attr("height", this.height() + this.margin.top + this.margin.bottom)
      .append("g")
      .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

    this.bases = {
      axes: {
        x : svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + this.height() + ")"),

        y : svg.append("g")
          .attr("class", "y axis")
      },

      paths: svg.append("g")
        .attr("class", "paths"),

      circles: svg.append("g")
        .attr("class", "circles")
    };

    this.bases.axes.ylabel = this.bases.axes.y.append("text")
      .attr("transform", "rotate(-90)")
      .classed("label", true)
      .attr("y", 10)
      .attr("dy", -this.margin.left)
      .attr("dx", "-100");

    this.scales = {
      x : d3.scale.ordinal()
        .rangeBands([0, this.width()])
        .domain(decades),
      y : d3.scale.linear()
      .range([this.height(), this.margin.top])
    };

    this.bases.circles
      .attr("transform", "translate("+ this.scales.x.rangeBand()/2 +","+ 0 +")");

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
        .tickSize(-this.width())
    };


    var chart = this;
    this.getX = function(d, idx) {
      return chart.scales.x(d[0]);
    };

    this.getY = function(d, idx) {
      if (chart.format() === 'total') return chart.scales.y(d[1]);
      if (chart.format() === 'decade') {
        return chart.scales.y(d[1] / chart.total_counts[idx][1]);
      }
      if (chart.format() === 'trope') return chart.scales.y(d[1] / chart.total_counts[d[2]]);

      return chart.scales.y(d[1]);
    };

    this.line = d3.svg.line()
      // .interpolate("cardinal")
      .x(this.getX)
      .y(this.getY);

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
          })
          .attr("d", chart.line);
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

    // circles and labels
    this.layer('circles', this.bases.circles
      .append("g").classed("circles1", true),
      {
        dataBind: function(data) {
          var chart = this.chart();
          if (chart._currentlySelected) {
            return this.selectAll('circle')
              .data(chart._currentlySelected.datum());
          } else {
            return this.selectAll('circle')
              .data([]);
          }
        },
        insert: function() {
          return this.append('circle');
        },
        events: {
          update : function(d) {
            var chart = this.chart();
            this.attr('cx', chart.getX)
              .attr('cy', chart.getY)
              .attr('r', 5);
          },
          exit: function() {
            this.remove();
          }
        }
      });

    this.layer('circle-labels', this.bases.circles.append("g")
      .classed("circles2", true),
      {
        dataBind: function(data) {
          var chart = this.chart();
          if (chart._currentlySelected) {
            return this.selectAll('text')
              .data(chart._currentlySelected.datum());
          } else {
            return this.selectAll('text')
              .data([]);
          }
        },
        insert: function() {
          return this.append('text');
        },
        events: {
          update : function(d) {
            var chart = this.chart();
            this.attr('x', chart.getX)
            .attr('y', function(d, i) {
              return chart.getY(d, i) - 10;
            })
            .attr('text-anchor', 'middle')
            .text(function(d, i) {
              if (chart.format() === 'total') {
                return Math.round(chart.scales.y.invert(chart.getY(d, i)));
              } else {
                return d3.format('0%')(chart.scales.y.invert(chart.getY(d, i)));
              }
            });
          },
          exit: function() {
            this.remove();
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
    var chart = this;
    if (this._currentlySelected) {
      this._currentlySelected.classed("selected", false);
    }

    if (name !== null) {
      var p = this.bases.paths.select("path[trope=" + name +"]")
        .classed("selected", true)
        .moveToFront();

      this._currentlySelected = p;
      chart.layer('circles').draw(p.datum());
      chart.layer('circle-labels').draw(p.datum());
    } else {
      this._currentlySelected = null;
      chart.layer('circles').draw([]);
      chart.layer('circle-labels').draw([]);
    }
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

    this.scales.y.domain([min,max]);

    // update y axis. X is fixed, because all decades.
    this.bases.axes.y.call(this.axes.y);

    // adjust label on y axis

    if (chart.format() === 'total') {
      this.bases.axes.ylabel.text("Total Count per Decade");
    }
    if (chart.format() === 'decade') {
      this.bases.axes.ylabel.text("% of Total Trope Occurance in Decade");
    }
    if (chart.format() === 'trope') {
      this.bases.axes.ylabel.text("% of Total Trope Occurance Over Time");
    }

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
