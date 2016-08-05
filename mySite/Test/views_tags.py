from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from MCEditor.views import editor
from .models import *
from django.shortcuts import render
from MCBase.views import *
from .views_detail import *

def addTag(request,questionContainer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    text = request.POST.get("tag-text")
    Tag.newTag(text)
    tag = Tag.objects.get(text=text)
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
    questionContainer.tags.add(tag)
    return editTag(request,questionContainer_pk)
def removeTag(request,questionContainer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    text = request.POST.get("tag-text")
    tag = Tag.objects.get(text=text)
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
    questionContainer.tags.remove(tag)
    questionContainer.save()
    # delete tag if it does not correspond to any question
    if tag.questionContainers.count() == 0:
        tag.delete()
    return editTag(request,questionContainer_pk)
def editTag(request,questionContainer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
    tags = questionContainer.tags.all()
    allTags = Tag.objects.all()
    context = {'questionContainer':questionContainer, 'tags':tags, 'allTags':allTags}
    return render(request, 'Test/editTag.html', context)


def adminTagsIndividual(request):
    #if not request.user.is_superuser: # TODO: add back in
    #    return HttpResponse("You are not a superuser")
    questionContainers = QuestionContainer.objects.all()
    for questionContainer in questionContainers:
        tags = Tag.objects.extra( select={'lower_text': 'lower(text)'}).order_by("lower_text").all() # tags sorted in alphabetical order
        questionContainer.taglist = tags
        for i,tag in enumerate(questionContainer.taglist):
            questionContainer.taglist[i].checked = tag in questionContainer.tags.all()
    context = {'questionContainers':questionContainers}
    return render(request, 'Test/adminTagsIndividual.html', context)
def adminTagsMass(request): # TODO: this is exactly the same as adminTagsIndividual outside of html
    #if not request.user.is_superuser: # TODO: add back in
    #    return HttpResponse("You are not a superuser")
    questionContainers = QuestionContainer.objects.all()
    for questionContainer in questionContainers:
        tags = Tag.objects.extra( select={'lower_text': 'lower(text)'}).order_by("lower_text").all() # tags sorted in alphabetical order
        questionContainer.taglist = tags
        for i,tag in enumerate(questionContainer.taglist):
            questionContainer.taglist[i].checked = tag in questionContainer.tags.all()
    context = {'questionContainers':questionContainers}
    return render(request, 'Test/adminTagsMass.html', context)

# Edits all tags for a single questionContainer
def selectTags(request,questionContainer_pk):
    tags = Tag.objects.all()
    for tag in tags:
        # tag is checked
        if request.POST.get(tag.text,False):
            questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
            questionContainer.tags.add(tag)
        else:
            questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
            questionContainer.tags.remove(tag)
    return HttpResponse("done")

# Edit all tags for all questionContainer
def selectAllTags(request):
    # clear all tags
    for questionContainer in QuestionContainer.objects.all():
        questionContainer.tags.clear()
    tags = Tag.objects.all()
    for tag in tags:
        vals = request.POST.getlist(tag.text)
        for val in vals:
            questionContainer = QuestionContainer.objects.get(pk=val)
            questionContainer.tags.add(tag)
    return HttpResponseRedirect(reverse('Test:adminTagsMass'))
