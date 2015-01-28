Util = {
  rankingMap : function(ranking) {
    var map = {};

    ranking[0].forEach(function(adjective) {
      map[adjective[0]] = adjective;
    });

    return map;
  },

  tropeMap: function(tropes, adjRankings) {
    var map = {};
    var max = 0;
    tropes[0].forEach(function(trope) {

      // get first letter
      var firstLetter = trope[0][0];
      var item = {
        name : trope[0],
        values: trope[1]
      };

      // for each adjective in the list, append the
      // score from the adjective ranking
      item.values = _.unique(item.values);
      item.values.forEach(function(adjective, i) {

        adjective = adjective.toLowerCase();
        var score = adjRankings[adjective][3];
        if (adjRankings[adjective]) {
          item.values[i] = [adjective, score];
        } else {
          item.values[i] = [adjective, -2];
        }
        max = Math.max(score, max);
      });

      item.values = _.sortBy(item.values, function(adj) {
        return -adj[1];
      });
      if (map[firstLetter]) {
        map[firstLetter].push(item);
      } else {
        map[firstLetter] = [item];
      }
    });

    var letters = _.range(65, 65+27);
    var arr = [];
    for (var i = 0; i < letters.length-1; i++) {
      var letter = String.fromCharCode(i + 65);
      if (typeof map[letter] !== "undefined") {
        arr[i] = { letter : letter, values : map[letter] };
      } else {
        arr[i] = { letter: letter, values : [] };
      }
    }

    console.log(max);
    return arr;
  }
};