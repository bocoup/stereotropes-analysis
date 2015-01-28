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
        scrollLeft: scrollToEl.offset().left
      }, 1000);
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

  var getData = function(gender) {
    var def = $.Deferred();

    var getTropeAdjectives = $.ajax('../../data/results/' + gender + '_tropes_adjectives.json');
    var getRanking = $.ajax('../../data/analysis/' + gender + '_ll.json');

    $.when(getTropeAdjectives, getRanking).done(function(tropes, adjectiveRanking) {

      // convert tropes and adjectives to map
      def.resolve(Util.tropeMap(tropes), Util.rankingMap(adjectiveRanking));

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