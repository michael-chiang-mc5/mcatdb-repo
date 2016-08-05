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
    return editTags(request,questionContainer_pk)
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
    return editTags(request,questionContainer_pk)
def editTags(request,questionContainer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
    tags = questionContainer.tags.all()
    allTags = Tag.objects.all()
    context = {'questionContainer':questionContainer, 'tags':tags, 'allTags':allTags}
    return render(request, 'Test/editTags.html', context)
