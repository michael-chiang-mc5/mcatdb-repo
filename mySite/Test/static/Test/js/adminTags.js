
// Submit answers
$(document).ready(function() {
  $('button').click(function() {
    var f = $(this).prev('form');
    var url = f.attr( 'action' );
    $.ajax({
      type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
      url         : url, // the url where we want to POST
      data        : f.serialize(), // our data object
      dataType    : 'json', // what type of data do we expect back from the server
                  encode          : true
    })


  });
});
