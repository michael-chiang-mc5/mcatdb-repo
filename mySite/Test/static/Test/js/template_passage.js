window.fresh = true

// Allow for de-selecting answers, turn selected answers blue
$(document).ready(function() {
  $('.answer-box').click(function() {

    if (fresh) {
      if ($(this).find('input:radio')[0].checked == true ) {
        $(this).find('input:radio')[0].checked = false;
        $(this).removeClass('selected-answer');
        event.stopPropagation();
      } else {
        $(this).find('input:radio')[0].checked = true;
        $(this).parent().children('.answer-box').removeClass('selected-answer');
        $(this).addClass('selected-answer');
        event.stopPropagation();
      }
    }

  });
});

// Submit answers
$(document).ready(function() {
  $('button').click(function() {

    // iterate through questions
    $(this).parent().children('.question-box').each(function () {
      var question_box = $(this)

      // check if an answer is selected
      if (question_box.children('.answer-box').hasClass('selected-answer')) {
        // iterate through answers
        question_box.children('.answer-box').each(function() {
          var answer_box = $(this)
          // if answer is correct, make question background green and display header-correct
          if (answer_box.hasClass('selected-answer') && answer_box.hasClass('answer-correct')) {
            question_box.children('.header-correct').show()
          }
          // if answer is incorrect, make question background red
          if (answer_box.hasClass('selected-answer') && answer_box.hasClass('answer-incorrect')) {
            question_box.children('.header-incorrect').show()
          }
        });
      } else {
        // no answer selected so incorrect
        question_box.children('.header-incorrect').show()
      }


    });


    // disable radio buttons, submit buttons
    $(this).hide()
    fresh = false


  });
});


// Toggle explanation
$(document).ready(function() {
  $('.toggle-explanation').click(function() {
    var answer_boxes = $(this).parent().siblings(".answer-box")
    answer_boxes.each(function () {
      var explanation = $(this).children(".explanation")
      explanation.toggle()
    });

  });
});

// Toggle edit mode
$(document).on('click', "#show-edit-tools", function(){
  $.ajax({
    type        : 'GET', // define the type of HTTP verb we want to use (POST for our form)
    url         : '/Test/showEditTools/', // the url where we want to POST
  }).done(function(data) {
    $('.admin-tools').show()
    $('.question-box').children('.header-correct').show()
    $('.question-box').children('.header-incorrect').show()
    $('.explanation').show()

  });
});
$(document).on('click', "#hide-edit-tools", function(){
  $.ajax({
    type        : 'GET', // define the type of HTTP verb we want to use (POST for our form)
    url         : '/Test/hideEditTools/', // the url where we want to POST
  }).done(function(data) {
    $('.admin-tools').hide()
    $('.question-box').children('.header-correct').hide()
    $('.question-box').children('.header-incorrect').hide()
    $('.explanation').hide()

  });
});

// Make passage/questions same height as the window
window_height = $(window).height()
function getHeight() {
  offset_height = $('.left-box').offset().top
  return window_height - offset_height
}
$(document).ready(function() {
  // set initial div height / width
  $('.left-box').css({
    'height': getHeight(),
  });
  $('.right-box').css({
    'height': getHeight(),
  });

});
