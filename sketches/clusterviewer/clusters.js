
function loadData(cb){
  $.when(
    $.getJSON('data/all_trope_clusters.json'),
    $.getJSON('data/female_trope_clusters.json'),
    $.getJSON('data/male_trope_clusters.json')
  ).then(function(all, female, male){
    console.log('data loaded', arguments);
    cb(all[0], female[0], male[0]);
  });
}

function render(all, male, female){

  function formatData(clusters) {
    var data = _.map(clusters['by_cluster'], function(val, key){
      var cluster_terms = clusters['cluster_description'][key]['terms'];
      var cluster_docs = val;
      return {
        'clusterTerms': cluster_terms,
        'clusterDocs': cluster_docs
      };
    });
    return data;
  }


  var data = {
    'all': formatData(all),
    'male': formatData(male),
    'female': formatData(female),
  };

  console.log('render data', data);

  var ractive = new Ractive({
    el: 'container',
    template: '#template',
    data: {
      clusters: data['all']
    }
  });


  $('#selector').change(function(){
    var davalue = $(this).val();
    ractive.set('clusters', data[davalue]);
  });
}


$(document).ready(function(){
  loadData(function(all, female, male){
    render(all, male, female);
  });
});
