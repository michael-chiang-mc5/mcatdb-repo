from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^deleteAnswer/(?P<answer_pk>[0-9]+)/$', views.deleteAnswer, name='deleteAnswer'),
    url(r'^deleteQuestion/(?P<question_pk>[0-9]+)/$', views.deleteQuestion, name='deleteQuestion'),
    url(r'^deletePassage/(?P<passage_pk>[0-9]+)/$', views.deletePassage, name='deletePassage'),


    url(r'^hideEditTools/$', views.hideEditTools, name='hideEditTools'),
    url(r'^showEditTools/$', views.showEditTools, name='showEditTools'),

    url(r'^randomQuestion/$', views.randomQuestion, name='randomQuestion'),

    url(r'^questionContainerList/$', views.questionContainerList, name='questionContainerList'),


    url(r'^questionContainerDetail/(?P<questionContainer_pk>[0-9]+)/(?P<showComments>[0-1]+)/$', views.questionContainerDetail, name='questionContainerDetail'),



    url(r'^selectAllTags/$', views.selectAllTags, name='selectAllTags'),


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

    url(r'^editTag/(?P<questionContainer_pk>[0-9]+)/$', views.editTag, name='editTag'),
    url(r'^addTag/(?P<questionContainer_pk>[0-9]+)/$', views.addTag, name='addTag'),
    url(r'^removeTag/(?P<questionContainer_pk>[0-9]+)/$', views.removeTag, name='removeTag'),


    url(r'^addComment/(?P<questionContainer_pk>[0-9]+)/$', views.addComment, name='addComment'),
    url(r'^editCommentEditor/(?P<comment_pk>[0-9]+)/$', views.editCommentEditor, name='editCommentEditor'),
    url(r'^editComment/(?P<comment_pk>[0-9]+)/$', views.editComment, name='editComment'),
    url(r'^deleteComment/(?P<comment_pk>[0-9]+)/$', views.deleteComment, name='deleteComment'),

    url(r'^copyQuestionContainer/(?P<questionContainer_pk>[0-9]+)/$', views.copyQuestionContainer, name='copyQuestionContainer'),
    url(r'^copyQuestionInPassage/(?P<question_pk>[0-9]+)/$', views.copyQuestionInPassage, name='copyQuestionInPassage'),

]
