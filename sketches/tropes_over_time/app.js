$(function() {
  var selectors = new Ractive({
    el: $('.genderSelector')[0],
    template: $('#tmp-selectors').text(),
    data: {
      genders : ['male','female'],
      formats: ['total', 'decade', 'trope']
    }
  });

  var reducer = function(vals, fn, prop, start) {
    return vals.reduce(function(prev, curr, indx, arr) {
      return fn(prev, curr[prop]);
    }, start);
  };

  var sorter = function(a, b) {
    return a.name > b.name ? 1 : (a.name < b.name ? -1 : 0);
  };

  var chartNode = d3.select('.visContainer');
  var subset = null;

  var chart = chartNode.chart('LineGraph', {
    format: 'trope',
    height: 600,
    width: $(chartNode.node()).width()
  });

  selectors.observe('selectedGender', function(g) {
    $.ajax('../../data/results/'+g+'_film_tropes.json').then(function(tropes) {

      //===== find min and max film count
      var max = reducer(tropes.values, Math.max, 'films_count', 0);
      var min = reducer(tropes.values, Math.min, 'films_count', Infinity);

      var occurance = new Ractive({
        el: $('.occuranceSelector')[0],
        template: $('#tmp-range').text(),
        data: {
          title: 'Frequency of Occurance',
          min: min,
          max: max,
          id: 'occurance_range',
          step: 10
        }
      });

      occurance.set('selectedOccurance', min);

      //===== find min and max film unique count
      max = reducer(tropes.values, Math.max, 'decade_counts_diff', 0);
      min = reducer(tropes.values, Math.min, 'decade_counts_diff', Infinity);

      var uniqueness = new Ractive({
        el: $('.uniqueFilmSelector')[0],
        template: $('#tmp-range').text(),
        data: {
          title: 'Variance in Diffs',
          min: min,
          max: max,
          id: 'variance',
          step: 10
        }
      });

      uniqueness.set('selectedOccurance', min);

      var tropeList = new Ractive({
        el: $('.list')[0],
        template: $('#tmp-tropes').text(),
        data: {
          tropes : tropes.values.sort(sorter),
          format: function(name) {
            return name.split(/(?=[A-Z])/).join(" ");
          }
        }
      });

      // filter tropes by film count
      occurance.observe('selectedOccurance', function(val) {
        uniqueness.set('selectedOccurance', 0);
        // filter the original data
        var subset = tropes.values.filter(function(trope) {
          return trope.films_count > val;
        }).sort(sorter);

        tropeList.set('tropes', subset);
        chart.highlight(null);
      });

      // filter tropes by decade_counts_diff
      uniqueness.observe('selectedOccurance', function(val) {
        occurance.set('selectedOccurance', 0);
        // filter the original data
        var subset = tropes.values.filter(function(trope) {
          return trope.decade_counts_diff > val;
        }).sort(sorter);
        tropeList.set('tropes', subset);
        chart.highlight(null);
      });

      tropeList.observe('tropes', function(data) {
        subset = data;
        chart.draw(data);
      });

      tropeList.on('select', function(event) {
        chart.highlight(event.context.name);
      });

      selectors.observe('selectedFormat', function(format) {
        chart.format(format);
        if (subset) chart.draw(subset);
        chart.highlight(null);
      });
    });
  });
});