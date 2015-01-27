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
        .orient('bottom'),
      y : d3.svg.axis()
        .scale(this.scales.y)
        .orient('left')
    };

    var chart = this;
    this.line = d3.svg.line()
      // .interpolate("cardinal")
      .x(function(d, i) { return chart.scales.x(d[0]); })
      .y(function(d, i) { return chart.scales.y(d[1]); }); // try to divide by total_counts[i][1]

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
        enter: function() {
          var chart = this.chart();
          this.attr("trope", function(d) {
            return d.name;
          }).datum(function(d) {
            return d.decade_counts;
          }).attr("d", chart.line);
        },
        "exit:transition": function() {
          this.attr('opacity', 0).remove();
        }
      }

    });
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
    var min = 0;
    var max = data.reduce(function(prev, current, index, array) {
      var y = d3.max(current.decade_counts, function(m, idx) {
        return m[1]; // / total_counts[idx][1];
      });
      var x = d3.max([prev, y]);
      return x;
    }, 0);

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
