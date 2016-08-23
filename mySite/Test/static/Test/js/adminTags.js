// show edit form when clicking edit
$(document).on('click', '.filter-tags', function(){
  var editform = $(this).next(".tag-choices")
  $(editform).toggle();
});
