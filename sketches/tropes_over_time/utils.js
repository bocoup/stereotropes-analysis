var decades = [
  'Films of the 1920s', 'Films of the 1930s', 'Films of the 1940s',
  'Films of the 1950s', 'Films of the 1960s', 'Films of the 1970s',
  'Films of the 1980s', 'Films of the 1990s', 'Films of the 2000s',
  'Films of the 2010s'
];

var aggregateData = function(data) {

  var min = 0;
  var formats = {
    'total' : {},
    'decade' : {},
    'trope': {}
  };

  var decade_counts = [];

  // ===  decade:
  // aggregate by decade [[decade, totalForDecade], ...]
  decades.forEach(function(decade) {
    decade_counts.push([decade, 0]);
  });

  data.forEach(function(d) {
    d.decade_counts.forEach(function(m, i) {
      decade_counts[i][1] += m[1];
    });
  });

  formats.decade.totals = decade_counts;

  // === trope
  // aggregate by trope
  trope_counts = {};
  data.forEach(function(d) {
    if (trope_counts[d.name]) {
      trope_counts[d.name] += d.films_count;
    } else {
      trope_counts[d.name] = d.films_count;
    }
  });

  formats.trope.totals = trope_counts;

  var maximiser = function(data, fn) {
    return data.reduce(function(prev, current, index, array) {
      var trope = current.name;
      var lmax = d3.max(current.decade_counts, function(m, idx) {
        return fn(m, idx, trope);
      }, 0);

      return d3.max([prev, lmax]);
    }, 0);
  };

  formats.total.range = [0, maximiser(data, function(m, idx) {
    return m[1];
  })];
  formats.decade.range = [0, maximiser(data, function(m, idx) {
    return m[1] / formats.decade.totals[idx][1];
  })];
  formats.trope.range = [0, maximiser(data, function(m, idx, trope) {
    return m[1] / formats.trope.totals[trope];
  })];

  return formats;
};