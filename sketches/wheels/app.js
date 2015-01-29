$(function() {
  var filters = new Ractive({
    el : $('.filterSelector')[0],
    template : $('#tmp-filters').text(),
    data : {
      genders: ['male','female'],
      letters: _.range(97, 123),
      toLetter: function(n) {
        return String.fromCharCode(n);
      }
    }
  });

  filters.observe('selectedLetter', function(idx, oldidx) {
    if (typeof idx === "undefined") {
      idx = 97;
    }

    var letter = String.fromCharCode(idx);
    var capitalLetter = String.fromCharCode(idx - 32);

    // highlight current letter in form
    var pos = idx - 96; //a is 97, reset to 1 pos

    // Reomve selected from current letter
    var current = $(this.el).find('h3.selected');
    if (current) current.removeClass('selected');

    // find new h3 and highlight it as selected.
    var h3 = $(this.el).find('h3:nth-child(' + pos + ')');
    h3.addClass('selected');

    // scroll the tropelist to the appropriate position
    var anchor = "#" + capitalLetter + "-letter";
    var scrollToEl = $(anchor);
    if (scrollToEl.size()) {
      $('html,body').stop().animate({
        scrollLeft: capitalLetter === 'A' ? 0 : scrollToEl.offset().left
      }, 1000);
    }
  });

  var tropeColor = d3.scale.linear()
    .domain([-1, -0.1, 0.2, 1])
    .range([
      "#7b3294",
      "#c2a5cf",
      "#a6dba0",
      "#008837"
    ]);
  var scoreForamtter = d3.format("0.2f");
  var tropeList = new Ractive({
    el: $('.list')[0],
    template: $('#tmp-tropes').text(),
    data: {
      tropes : [],
      format: function(name) {
        return name.split(/(?=[A-Z])/).join(" ");
      },
      formatScore: function(score) {
        return scoreForamtter(score);
      },
      color: function(score) {
        return tropeColor(score);
      }
    }
  });

  var getData = function(gender) {
    var def = $.Deferred();

    var getTropeAdjectives = $.ajax('../../data/analysis/' + gender + '_trope_ll.json');

    $.when(getTropeAdjectives).done(function(tropes) {

      // convert tropes and adjectives to map
      tropes = Util.tropeMap(tropes);
      def.resolve(tropes);

    });

    return def.promise();
  };

  filters.observe('selectedGender', function(gender) {
    getData(gender).then(function(tropeAdjectives, adjectiveRank) {

      // render tropes
      tropeList.set('tropes', tropeAdjectives);
    });
  });

});