from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from MCEditor.views import editor
from .models import *
from django.shortcuts import render
from MCBase.views import *
from .views_detail import *

# Methods to add and edit answers
def addAnswerEditor(request,question_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:addAnswer')
    form_data = serialize_json({'question_pk':question_pk,})
    header = "Add an answer"
    initial_text = ""
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def addAnswer(request):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    # save answer
    form_text = request.POST.get("form-text")
    answer = Answer(text=form_text)
    answer.save()
    # get question and add answer
    serialized_form_data = request.POST.get("serialized-form-data")
    form_data = deserialize_json_string(serialized_form_data)
    question_pk = int(form_data["question_pk"])
    question = Question.objects.get(pk=question_pk)
    question.answers.add(answer)
    # return view
    return recurseQuestionContainerDetail(request,answer)

def editAnswerEditor(request,answer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editAnswer',args=[answer_pk])
    form_data = {}
    header = "Edit an answer"
    # get initial text
    answer = Answer.objects.get(pk=answer_pk)
    initial_text = answer.text
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editAnswer(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get answer text
    form_text = request.POST.get("form-text")
    answer = Answer.objects.get(pk=answer_pk)
    answer.text = form_text
    # save
    answer.save()
    return recurseQuestionContainerDetail(request,answer)
def editExplanationEditor(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editExplanation',args=[answer_pk])
    form_data = {}
    header = "Edit an explanation"
    # get initial text
    answer = Answer.objects.get(pk=answer_pk)
    initial_text = answer.explanation
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editExplanation(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get answer text
    form_text = request.POST.get("form-text")
    answer = Answer.objects.get(pk=answer_pk)
    answer.explanation = form_text
    # save
    answer.save()
    return recurseQuestionContainerDetail(request,answer)

def deleteAnswer(request,answer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    answer = Answer.objects.get(pk=answer_pk)
    question_pk = answer.question_pk()
    question = Question.objects.get(pk=question_pk)
    answer.delete()
    return recurseQuestionContainerDetail(request,question)


def markAnswerCorrect(request,answer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    answer = Answer.objects.get(pk=answer_pk)
    answer.correct = True
    answer.save()
    return recurseQuestionContainerDetail(request,answer)
def markAnswerIncorrect(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    answer = Answer.objects.get(pk=answer_pk)
    answer.correct = False
    answer.save()
    return recurseQuestionContainerDetail(request,answer)
