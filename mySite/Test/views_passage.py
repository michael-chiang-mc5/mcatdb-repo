from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from MCEditor.views import editor
from .models import *
from django.shortcuts import render
from .views_detail import *




def addPassageEditor(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:addPassage')
    form_data = {}
    header = "Add a passage"
    initial_text = ""
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def addPassage(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    form_text = request.POST.get("form-text")
    passage = Passage(text=form_text)
    passage.save()
    # add questionContainer
    questionContainer = QuestionContainer(content_object=passage)
    questionContainer.save()
    return recurseQuestionContainerDetail(request, questionContainer)

def editPassageEditor(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editPassage',args=[passage_pk])
    form_data = {}
    header = "Edit a passage"
    # get initial text
    passage = Passage.objects.get(pk=passage_pk)
    initial_text = passage.text
    # return editor
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editPassage(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    form_text = request.POST.get("form-text")
    passage = Passage.objects.get(pk=passage_pk)
    passage.text = form_text
    passage.save()
    return recurseQuestionContainerDetail(request, passage)

def deletePassage(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    passage = Passage.objects.get(pk=passage_pk)
    passage.delete()
    return HttpResponseRedirect( reverse('Test:questionContainerList') )
