from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^deleteAnswer/(?P<answer_pk>[0-9]+)/$', views.deleteAnswer, name='deleteAnswer'),
    url(r'^deleteQuestion/(?P<question_pk>[0-9]+)/$', views.deleteQuestion, name='deleteQuestion'),
    url(r'^deletePassage/(?P<passage_pk>[0-9]+)/$', views.deletePassage, name='deletePassage'),

    url(r'^hideEditTools/$', views.hideEditTools, name='hideEditTools'),
    url(r'^showEditTools/$', views.showEditTools, name='showEditTools'),

    url(r'^randomQuestion/$', views.randomQuestion, name='randomQuestion'),

    url(r'^submitPassageAnswers/$', views.submitPassageAnswers, name='submitPassageAnswers'),


    url(r'^passageList/$', views.passageList, name='passageList'),
    url(r'^passageDetail/(?P<passage_pk>[0-9]+)/$', views.passageDetail, name='passageDetail'),

    url(r'^standaloneQuestionList/$', views.standaloneQuestionList, name='standaloneQuestionList'),
    url(r'^standaloneQuestionDetail/(?P<question_pk>[0-9]+)/$', views.standaloneQuestionDetail, name='standaloneQuestionDetail'),
    url(r'^questionUserView/(?P<question_pk>[0-9]+)/$', views.questionUserView, name='questionUserView'),


    url(r'^adminPanel/$', views.adminPanel, name='adminPanel'),
    url(r'^adminList/$', views.adminList, name='adminList'),

    # add or edit passages
    url(r'^addPassage/$', views.addPassage, name='addPassage'),
    url(r'^addPassageEditor/$', views.addPassageEditor, name='addPassageEditor'),
    url(r'^editPassage/(?P<passage_pk>[0-9]+)/$', views.editPassage, name='editPassage'),
    url(r'^editPassageEditor/(?P<passage_pk>[0-9]+)/$', views.editPassageEditor, name='editPassageEditor'),
    url(r'^editPassageAdminNotes/(?P<passage_pk>[0-9]+)/$', views.editPassageAdminNotes, name='editPassageAdminNotes'),
    url(r'^editPassageAdminNotesEditor/(?P<passage_pk>[0-9]+)/$', views.editPassageAdminNotesEditor, name='editPassageAdminNotesEditor'),

    # add or edit questions
    url(r'^addQuestionEditor/(?P<passage_pk>[0-9]+)/$', views.addQuestionEditor, name='addQuestionEditor'),
    url(r'^addQuestion/$', views.addQuestion, name='addQuestion'),
    url(r'^editQuestionEditor/(?P<question_pk>[0-9]+)/$', views.editQuestionEditor, name='editQuestionEditor'),
    url(r'^editQuestion/(?P<question_pk>[0-9]+)/$', views.editQuestion, name='editQuestion'),
    url(r'^editQuestionAdminNotesEditor/(?P<question_pk>[0-9]+)/$', views.editQuestionAdminNotesEditor, name='editQuestionAdminNotesEditor'),
    url(r'^editQuestionAdminNotes/(?P<question_pk>[0-9]+)/$', views.editQuestionAdminNotes, name='editQuestionAdminNotes'),


    # add or edit answers
    url(r'^addAnswerEditor/(?P<question_pk>[0-9]+)/$', views.addAnswerEditor, name='addAnswerEditor'),
    url(r'^addAnswer/$', views.addAnswer, name='addAnswer'),
    url(r'^editAnswerEditor/(?P<answer_pk>[0-9]+)/$', views.editAnswerEditor, name='editAnswerEditor'),
    url(r'^editAnswer/(?P<answer_pk>[0-9]+)/$', views.editAnswer, name='editAnswer'),
    url(r'^editExplanationEditor/(?P<answer_pk>[0-9]+)/$', views.editExplanationEditor, name='editExplanationEditor'),
    url(r'^editExplanation/(?P<answer_pk>[0-9]+)/$', views.editExplanation, name='editExplanation'),
    url(r'^markAnswerCorrect/(?P<answer_pk>[0-9]+)/$', views.markAnswerCorrect, name='markAnswerCorrect'),
    url(r'^markAnswerIncorrect/(?P<answer_pk>[0-9]+)/$', views.markAnswerIncorrect, name='markAnswerIncorrect'),

    url(r'^editTags/(?P<question_pk>[0-9]+)/$', views.editTags, name='editTags'),
    url(r'^addTag/(?P<question_pk>[0-9]+)/$', views.addTag, name='addTag'),
    url(r'^removeTag/(?P<question_pk>[0-9]+)/$', views.removeTag, name='removeTag'),


]
