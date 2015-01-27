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

d3.chart("GraphBase", {
  initialize: function(options) {
    this.format(options.format || 'total', options.formatRanges);

    this.margin = {
      top: 20, right: 20, bottom: 30, left: 50
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
      return d[0];
    };

    this.getY = function(d, idx) {
      if (chart.format() === 'total') {
        return d[1];
      }
      if (chart.format() === 'decade') {
        return d[1] / chart.formatRange().totals[idx][1];
      }
      if (chart.format() === 'trope') {
        return d[1] / chart.formatRange().totals[d[2]];
      }
    };

    // render x axis (it will never change)
    this.bases.axes.x.call(this.axes.x);

  },

  // Displaying values. Options are:
  // total - raw counts
  // decade - this tropes utilization over that decade across all tropes
  // trope - this tropes utilization in that decade over time
  // ranges - object containing all three , their totals (if they exist)
  //   and a range for em.
  format: function(name, ranges) {
    if (arguments.length) {
      this._format = name;
      if (ranges) {
        this._ranges = ranges;
      }
      return this;
    } else {
      return this._format;
    }
  },

  formatRange: function(name) {
    if (arguments.length) {
      return this._ranges[name];
    } else {
      return this._ranges[this._format];
    }
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
  },

  transform: function(data) {
    var chart = this;
    var min = 0;

    // pin the y domain to the current format
    this.scales.y.domain(this.formatRange().range);

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
  }


});

d3.chart("GraphBase").extend("AreaGraph", {
  initialize: function(options) {
    var chart = this;

    this.base.classed("areagraph", true);

    this.stack = d3.layout.stack()
      .offset("expanded")
      .values(function(d) { return d.decade_counts; })
      .x(function(d, i) { return chart.getX(d, i); })
      .y(function(d, i) { return chart.getY(d, i); });


    this.area = d3.svg.area()
      .interpolate("cardinal")
      .x(function(d, i) {
        return chart.scales.x(d[0]);
      })
      .y0(function(d, i) {
        return chart.scales.y(d.y0);
      })
      .y1(function(d, i) {
        return chart.scales.y(d.y0 + d.y);
      });

    this.scales.color = d3.scale.category20b();
    this.layer('layers', this.bases.paths, {
      dataBind: function(data) {
        var chart = this.chart();
        data = chart.stack(data);

        // update scales... this sucks
        var max = data.reduce(function(prev, current, index, array) {
          var trope = current.name;
          var y = d3.max(current.decade_counts, function(m, idx) {
            return m.y0 + m.y;
          });
          var x = d3.max([prev, y]);
          return x;
        }, 0);

        chart.scales.y.domain([0, max]);

        return this.selectAll('path')
          .data(data, function(d) {
            return d.name;
          });
      },
      insert: function() {
        var chart = this.chart();
        return this.append('path')
          .attr("class", "layer")
          .attr("transform", "translate("+ chart.scales.x.rangeBand()/2 +","+ 0 +")");
      },
      events: {
        enter: function() {
          var chart = this.chart();

          this.style("fill", function(d, i) {
            return chart.scales.color(i);
          }).attr("trope", function(d) {
            return d.name;
          }).datum(function(d) {
            return d.decade_counts;
          })
          .attr("d", chart.area);
        },
        update: function() {
          var chart = this.chart();
          // this.attr("d", function(d)  {
          //   return chart.area(d.decade_counts);
          // })
          this.datum(function(d) {
            return d.decade_counts;
          })
          .attr("d", chart.area);
        },
        exit: function() {
          this.remove();
        }
      }
    });
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
      // chart.layer('circles').draw(p.datum());
      // chart.layer('circle-labels').draw(p.datum());
    } else {
      this._currentlySelected = null;
      // chart.layer('circles').draw([]);
      // chart.layer('circle-labels').draw([]);
    }
    return this;

  }

});

d3.chart("GraphBase").extend("LineGraph", {

  initialize: function(options) {
    var chart = this;

    this.base.classed("linegraph", true);
    this.line = d3.svg.line()
      .interpolate("cardinal")
      .x(function(d,i) { return chart.scales.x(chart.getX(d,i)); })
      .y(function(d,i) { return chart.scales.y(chart.getY(d,i)); });

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
            this.attr('cx', function(d, i) {
              return chart.scales.x(chart.getX(d,i));
            }).attr('cy', function(d, i) {
              return chart.scales.y(chart.getY(d,i));
            })
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
            this.attr('x', function(d, i) {
              return chart.scales.x(chart.getX(d,i));
            })
            .attr('y', function(d, i) {
              return chart.scales.y(chart.getY(d, i)) - 10;
            })
            .attr('text-anchor', 'middle')
            .text(function(d, i) {
              if (chart.format() === 'total') {
                return Math.round(chart.getY(d, i));
              } else {
                return d3.format('0.1%')(chart.getY(d, i));
              }
            });
          },
          exit: function() {
            this.remove();
          }
        }
      });
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
  }

});
