Util = {
  tropeMap: function(tropes) {
    var map = {};
    var max = 0;

    var trope_name, adjectives = [];

    tropes.forEach(function(trope) {

      trope_name = trope[0];
      adjectives = trope[1];

      // get first letter
      var firstLetter = trope_name[0];
      var item = {
        name : trope_name,
        values: adjectives
      };

      // for each adjective in the list, append the
      // score from the adjective ranking
      item.values.forEach(function(adjective, i) {

        adjective = adjective[0].toLowerCase();
        var score = adjective[3];

        max = Math.max(score, max);
      });

      // sort by normalized score
      item.values = _.sortBy(item.values, function(adj) {
        return -adj[3];
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

    return arr;
  }
};