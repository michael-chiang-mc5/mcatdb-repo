from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^passageList/$', views.passageList, name='passageList'),
    url(r'^passageDetail/(?P<passage_pk>[0-9]+)/$', views.passageDetail, name='passageDetail'),

    url(r'^standaloneQuestionList/$', views.standaloneQuestionList, name='standaloneQuestionList'),
    url(r'^questionDetail/(?P<question_pk>[0-9]+)/$', views.questionDetail, name='questionDetail'),
    url(r'^questionUserView/(?P<question_pk>[0-9]+)/$', views.questionUserView, name='questionUserView'),


    url(r'^adminPanel/$', views.adminPanel, name='adminPanel'),

    # add or edit passages
    url(r'^addPassage/$', views.addPassage, name='addPassage'),
    url(r'^addPassageEditor/$', views.addPassageEditor, name='addPassageEditor'),
    url(r'^editPassage/(?P<passage_pk>[0-9]+)/$', views.editPassage, name='editPassage'),
    url(r'^editPassageEditor/(?P<passage_pk>[0-9]+)/$', views.editPassageEditor, name='editPassageEditor'),

    # add or edit questions
    url(r'^addQuestionEditor/(?P<passage_pk>[0-9]+)/$', views.addQuestionEditor, name='addQuestionEditor'),
    url(r'^addQuestion/$', views.addQuestion, name='addQuestion'),
    url(r'^editQuestionEditor/(?P<question_pk>[0-9]+)/$', views.editQuestionEditor, name='editQuestionEditor'),
    url(r'^editQuestion/(?P<question_pk>[0-9]+)/$', views.editQuestion, name='editQuestion'),

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
