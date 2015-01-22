
function drawSplits(female, male) {

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

  function renderCorpus(corpus, label) {
    var data = _.filter(corpus, function(tuple) {
      return tuple[1] >= minOccurrences && tuple[3] > minLL;
    });
    console.log('renderCorpus', label, data.length);

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
          return cols(label);
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
        });

  }

  initCanvas();
  initScales(female, male);
  renderCorpus(female, 'Female');
  renderCorpus(male, 'Male');
}

function loadData(cb) {
  $.when(
    $.getJSON('data/female_ll.json'),
    $.getJSON('data/male_ll.json')
  ).then(function(female, male){
    console.log('data loaded')
    cb(female[0], male[0]);
  });
}


$(document).ready(function(){
  loadData(function(female, male){
    drawSplits(female, male);
  });
});