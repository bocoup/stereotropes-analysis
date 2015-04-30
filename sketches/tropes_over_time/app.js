$(function() {

  var chartNode = d3.select('.visContainer');

  var subset = null;
  var fulldata = null;
  var chart = null;
  var currentGender = null;
  var currentVisType = 'LineGraph';

  // gender, format and type of chart selectors
  var selectors = new Ractive({
    el: $('.genderSelector')[0],
    template: $('#tmp-selectors').text(),
    data: {
      genders : ['male','female'],
      formats: ['total', 'decade', 'trope']
    }
  });

  // when format changes, redraw with new format
  selectors.observe('selectedFormat', function(format) {
    if (chart) {
      chart.format(format);
      if (subset) {
        chart.draw(subset);
      };
      chart.highlight(null);
    }

  });

  // when area toggle switched, switch to line chart
  selectors.observe('isArea', function(val) {
    if (val)
      currentVisType = 'AreaGraph';
    else currentVisType = 'LineGraph';
    if (fulldata) {
      onData(fulldata);
    }
  });

  var occurance = new Ractive({
    el: $('.occuranceSelector')[0],
    template: $('#tmp-range').text(),
    data: {
      title: 'Frequency of Occurance',
      min: 0,
      max: 100,
      id: 'occurance_range',
      step: 10
    }
  });

  var uniqueness = new Ractive({
    el: $('.uniqueFilmSelector')[0],
    template: $('#tmp-range').text(),
    data: {
      title: 'Variance in Diffs',
      min: 0,
      max: 100,
      id: 'variance',
      step: 10
    }
  });

  // filter tropes by film count
  occurance.observe('selectedOccurance', function(val) {
    uniqueness.set('selectedOccurance', 0);

    if (fulldata && chart) {
      // filter the original data
      var subset = fulldata.values.filter(function(trope) {
        return trope.films_count >= val;
      }).sort(sorter);

      tropeList.set('tropes', subset);
      chart.highlight(null);
    }
  });

   // filter tropes by decade_counts_diff
  uniqueness.observe('selectedOccurance', function(val) {
    occurance.set('selectedOccurance', 0);

    if (fulldata && chart) {
      // filter the original data
      var subset = fulldata.values.filter(function(trope) {
        return trope.decade_counts_diff >= val;
      }).sort(sorter);

      tropeList.set('tropes', subset);
      chart.highlight(null);
    }
  });

  var tropeList = new Ractive({
    el: $('.list')[0],
    template: $('#tmp-tropes').text(),
    data: {
      tropes : [],
      format: function(name) {
        return name.split(/(?=[A-Z])/).join(" ");
      }
    }
  });

  tropeList.observe('tropes', function(data) {
    if (chart) {
      subset = data;
      chart.draw(data);
    }
  });

  tropeList.on('select', function(event) {
    chart.highlight(event.context.name);
  });

  var reducer = function(vals, fn, prop, start) {
    return vals.reduce(function(prev, curr, indx, arr) {
      return fn(prev, curr[prop]);
    }, start);
  };

  var sorter = function(a, b) {
    return a.name > b.name ? 1 : (a.name < b.name ? -1 : 0);
  };

  var getData = function(gender, callback) {
    return $.ajax('../../data/results/films/trope_films-' + gender + '.json')
      .then(callback);
  };

  var onData = function(tropes) {

    fulldata = tropes;

    // clear current vis
    $(chartNode.node()).empty();

    // get ranges for current nodes
    var range_maximums = aggregateData(tropes.values);

    // make a new graph
    chart = chartNode.chart(currentVisType, {
      format: 'total',
      formatRanges: range_maximums,
      height: 600,
      width: $(chartNode.node()).width()
    });

    //===== find min and max film count
    var max = reducer(tropes.values, Math.max, 'films_count', 0);
    var min = reducer(tropes.values, Math.min, 'films_count', Infinity);

    occurance.set('min', min);
    occurance.set('max', max);
    occurance.set('selectedOccurance', min);

    //===== find min and max film unique count
    max = reducer(tropes.values, Math.max, 'decade_counts_diff', 0);
    min = reducer(tropes.values, Math.min, 'decade_counts_diff', Infinity);

    uniqueness.set('min', min);
    uniqueness.set('max', max);
    uniqueness.set('selectedOccurance', min);

    tropeList.set('tropes', tropes.values.sort(sorter));

  };

  // when gender changes, get new data, paint all the things.
  selectors.observe('selectedGender', function(g) {
    currentGender = g;
    getData(currentGender, onData);
  });
});