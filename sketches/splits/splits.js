function buildAdjToTropes(femaleTropesToAdj, maleTropesToAdj) {
  var result = {};

  var tropesToAdj = femaleTropesToAdj.concat(maleTropesToAdj);

  _.each(tropesToAdj, function(trope){
    _.each(trope[1], function(adjective){
      var adj = adjective.toLowerCase();
      if(_.isUndefined(result[adj])){
        result[adj] = [];
      }
      result[adj].push(trope);
    });
  });

  return result;
}


function buildTropeList(tropeToAdj, withAdjectives) {
  var list = _.map(tropeToAdj, function(trope){
    if(_.isUndefined(withAdjectives)){
      return trope[0];
    } else {
      if(_.intersection(trope[1], withAdjectives).length > 0){
        return trope[0];
      }
    }
  });
  return _.compact(list);
}

function drawSplits(female, male, femaleTropesToAdj, maleTropesToAdj) {

  var width = 1600;
  var height = 800;


  var exp = 0.25;
  var minLL = 0.01;
  var minOccurrences = 5;

  var cols = d3.scale.category10()
    .domain(['Female', 'Male']);

  var xLeft = d3.scale.pow().exponent(exp)
    .domain([1, minLL])
    .range([0, width/2]);

  var xRight = d3.scale.pow().exponent(exp)
    .domain([minLL, 1])
    .range([width/2, width]);

  var fontSizeLeft = d3.scale.linear()
    .range([14, 60]);

  var fontSizeRight = d3.scale.linear()
    .range([14, 60]);

  var y = function() {
    return Math.random() * height;
  };

  function initScales(female, male) {
    var femaleCounts = _.map(female, function(tuple){
      return tuple[1];
    });

    var maleCounts = _.map(male, function(tuple){
      return tuple[1];
    });

    fontSizeLeft.domain(d3.extent(femaleCounts));
    fontSizeRight.domain(d3.extent(male));
  }

  function initCanvas() {
    var canvas = d3.select('#vis')
      .style('width', width + 'px')
      .style('height', height + 'px')
      .style('background-color', '#eee')
      .style('position', 'absolute')
      .style('left', '0px')
      .style('top', '0px');

    canvas.append('div')
      .attr('class', 'female')
      .style('width', width/2 + 'px')
      .style('height', height + 'px')
      .style('background-color', '#eee')
      .style('position', 'absolute')
      .style('left', '0px')
      .style('top', '0px');

    canvas.append('div')
      .attr('class', 'male')
      .style('width', width/2 + 'px')
      .style('height', height + 'px')
      .style('background-color', '#ddd')
      .style('position', 'absolute')
      .style('left', width/2 + 'px')
      .style('top', '0px');
  }

  function renderCorpus(corpus, label, otherCorpus) {
    var data = corpus;

    var otherCorpAjd = _.uniq(_.flatten(_.map(otherCorpus, function(t) { return t[1]; })));

    console.log('renderCorpus', label, data.length);

    console.log('otherCorpAjd', otherCorpAjd)

    corpus_group = d3.selectAll('#vis')
      .append('div')
        .attr('class', label)
      .data(data);

    corpus_group.enter()
      .append('div')
        .attr('class', 'token')
        .style('position', 'absolute')
        .style('left', function(d,i) {
          if(label === 'Female') {
            return xLeft(d[3]) + 'px';
          } else {
            return xRight(d[3]) + 'px';
          }
        })
        .style('top', function(d,i) {
          return y() + 'px';
        })
        .style('color', function(d,i) {
          console.log(d[0])
          if(_.contains(otherCorpAjd, d[0])){
            return cols(label);
          } else {
            if(label === 'Female') {
              return 'blue';
            } else {
              return 'red';
            }
          }
        })
        .style('font-size', function(d,i) {
          if(label === 'Female') {
            return fontSizeLeft(d[1]) + 'px';
          } else {
            return fontSizeRight(d[1]) + 'px';
          }
        })
        .text(function(d,i) {
          return d[0]// + d[3].toFixed(4);
        })
        .on('mouseenter', function(d){
          var tropes = adjToTropes[d[0]];
          tropes = _.uniq(_.map(tropes, function(t){
            return t[0];
          }));
          highlightTropes(tropes)

        });
  }


  function renderTropeList(tropeList, label) {
     var data = tropeList;

    console.log('renderTropeList', label, data.length);

    corpus_group = d3.selectAll('#vis .' + label)
      .append('div')
        .attr('class', label + '-tropes')
      .data(data);

    corpus_group.enter()
      .append('div')
        .attr('class', function(d, i){
          return 'trope-token ' + d;
        })
        .style('position', 'absolute')
        .style('left', function(d,i) {
          if(label === 'Female') {
            return 0 + 'px';
          } else {
            return width + 'px';
          }
        })
        .style('text-align', function(d,i) {
          if(label === 'Female') {
            return 'left';
          } else {
            return 'right';
          }
        })
        .style('top', function(d,i) {
          return (i*12) + 'px';
        })
        .style('color', function(d,i) {
          return 'black';
        })
        .style('font-size', function(d,i) {
          return '10px';
        })
        .text(function(d,i) {
          return d;
        });
  }

  function highlightTropes(tropes) {
    d3.selectAll('.highlighted')
      .classed('highlighted', false);

    _.each(tropes, function(trope){
      console.log("HIHIH", trope)
      d3.selectAll('.trope-token.' + trope)
        .classed('highlighted', true);
    });

    console.log("Highlighting", tropes);
  }

  var adjToTropes = buildAdjToTropes(femaleTropesToAdj, maleTropesToAdj);


  var maleCorpus = _.filter(male, function(tuple) {
    return tuple[1] >= minOccurrences && tuple[3] > minLL;
  });

  var femaleCorpus = _.filter(female, function(tuple) {
    return tuple[1] >= minOccurrences && tuple[3] > minLL;
  });

  var maleTropeList = buildTropeList(maleTropesToAdj, _.map(maleCorpus, function(tuple){
    return tuple[0];
  }));

  var femaleTropeList = buildTropeList(femaleTropesToAdj, _.map(femaleCorpus, function(tuple){
    return tuple[0];
  }));

  initCanvas();
  initScales(femaleCorpus, maleCorpus);
  renderCorpus(femaleCorpus, 'Female', maleTropesToAdj);
  renderCorpus(maleCorpus, 'Male', femaleTropesToAdj);

  renderTropeList(femaleTropeList, 'Female');
  renderTropeList(maleTropeList, 'Male');
}

function loadData(cb) {
  $.when(
    $.getJSON('data/female_ll.json'),
    $.getJSON('data/male_ll.json'),
    $.getJSON('data/female_tropes_adjectives.json '),
    $.getJSON('data/male_tropes_adjectives.json')
  ).then(function(female, male, femaleTropesToAdj, maleTropesToAdj){
    console.log('data loaded', arguments)
    cb(female[0], male[0], femaleTropesToAdj[0], maleTropesToAdj[0]);
  });
}


$(document).ready(function(){
  loadData(function(female, male, femaleTropesToAdj, maleTropesToAdj){
    drawSplits(female, male, femaleTropesToAdj, maleTropesToAdj);
  });
});