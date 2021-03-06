
// Allow for de-selecting answers, turn selected answers blue
$(document).ready(function() {
  $('.answer-box').click(function() {
    if ( !$(this).hasClass("unfresh") ) {
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

    // show comments
    $('.user-comments').show()
    // disable submit button that was clicked
    $(this).hide()

    // get question_box
    var question_box = $(this).parent()


    // logic for free response submission
    if ( question_box.hasClass( "free_response" ) ) {
      var user_answer = question_box.children('textarea').val().trim()
      // check user answer against correct answers
      var correct = false
      question_box.children('.answer-box').each(function() {
        var answer_text = $(this).children('.text-only').text().trim()
        if (user_answer == answer_text) {
          correct = true
        }
      });
      // display whether user is correct/incorrect
      if (correct) {
        question_box.children('.header-correct').show()
      } else {
        question_box.children('.header-incorrect').show()
      }
      // display correct answer
      var correct_answer = question_box.children('.displayed-answer')
      correct_answer.show()



    // logic for multiple choice submission
    } else if ( question_box.hasClass( "multiple_choice" ) ) {
      // bold correct answers
      question_box.children('.answer-box').each(function() {
        var answer_box = $(this)
        // disable selecting answers
        answer_box.addClass( "unfresh" )
        if (answer_box.hasClass('answer-correct')) {
          answer_box.css("font-weight","Bold");
          answer_box.css("font-size","18px");
          // mathjax must be set bold separately
          answer_box.find('.math').each(function() {
            $(this).css("font-weight","Bold");
          });
        }
      });
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
    }


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
    $('.question-box').children('.free-response-answer').show()
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
    $('.question-box').children('.free-response-answer').hide()
    $('.explanation').hide()

  });
});

// Make passage/questions same height as the window
window_height = $(window).height()
function getMaxHeight(el) {
  offset_height = $(el).offset().top
  return window_height - offset_height
}
$(document).ready(function() {


  try {
    var left_box = $('.left-box')
    var right_box = $('.right-box')
    var left_height = Math.min(getMaxHeight(left_box), left_box.height()   );
    var right_height = Math.min(getMaxHeight(right_box), right_box.height() + 10 );
    var height = Math.max(left_height,right_height)
    $('.left-box').css({
      'height': height,
    });
    $('.right-box').css({
      'height': height,
    });
  } catch(err) {

  }

});

// Toggle comment form
$(document).ready(function() {
  $('.toggle-comment').click(function() {
    $(this).parent().siblings(".comment-form").toggle()
  });
});


$(document).ready(function() {
  $('.highlight-comment').click(function() {
    var pk = $(this).attr('id')
    var sel = $('#comment-'+pk)


    $('.comment-box').css({
      'background-color': '#F5F5F5',
    })

    sel.css({
      'background-color': 'yellow',
    });
    sel.effect("shake", {}, 700);

  });
});
