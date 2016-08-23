from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from MCEditor.views import editor
from .models import *
from django.shortcuts import render
from MCBase.views import *
from .views_detail import *

# passage_pk = 0 if question is single
def addQuestionEditor(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:addQuestion')
    form_data = serialize_json({'passage_pk':passage_pk,})
    header = "Add a question"
    initial_text = ""
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def addQuestion(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get question text
    form_text = request.POST.get("form-text")
    question = Question(text=form_text)
    # get passage corresponding to question
    serialized_form_data = request.POST.get("serialized-form-data")
    form_data = deserialize_json_string(serialized_form_data)
    passage_pk = int(form_data["passage_pk"])
    question.save()

    # check if question corresponds to a passage
    # if so, add question to passage
    # otherwise, make sure to create questionContainer
    if passage_pk != 0:
        passage = Passage.objects.get(pk=passage_pk)
        passage.questions.add(question)
        passage.save()
    else:
        questionContainer = QuestionContainer(content_object=question)
        questionContainer.save()
    return recurseQuestionContainerDetail(request, question)

def editQuestionEditor(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editQuestion',args=[question_pk])
    form_data = {}
    header = "Edit a question"
    # get initial text
    question = Question.objects.get(pk=question_pk)
    initial_text = question.text
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editQuestion(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get question text
    form_text = request.POST.get("form-text")
    question = Question.objects.get(pk=question_pk)
    question.text=form_text
    # save
    question.save()
    return recurseQuestionContainerDetail(request, question)

def deleteQuestion(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    question = Question.objects.get(pk=question_pk)
    questionContainer_pk = question.questionContainer_pk()
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)

    if questionContainer.type() == "question":
        question.delete()
        return HttpResponseRedirect( reverse('Test:questionContainerList') )
    else:
        question.delete()
        return recurseQuestionContainerDetail(request, questionContainer)
