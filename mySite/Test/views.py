from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
from MCEditor.views import editor
from MCBase.views import *
from .views_admin import *
from .views_passage import *
from .views_question import *
from .views_detail import *
from .views_answer import *
from .views_tags import *

def adminTags(request):
    #if not request.user.is_superuser: # TODO: add back in
    #    return HttpResponse("You are not a superuser")
    questionContainers = QuestionContainer.objects.all()

    for questionContainer in questionContainers:
        tags = Tag.objects.extra( select={'lower_text': 'lower(text)'}).order_by("lower_text").all() # tags sorted in alphabetical order
        questionContainer.taglist = tags
        for i,tag in enumerate(questionContainer.taglist):
            questionContainer.taglist[i].checked = tag in question.tags.all()
    context = {'questionContainers':questionContainers}
    return render(request, 'Test/adminTags.html', context)

def showEditTools(request):
    userProfile = request.user.userprofile
    userProfile.seeAdminTools = True
    userProfile.save()
    return HttpResponse("done")
def hideEditTools(request):
    userProfile = request.user.userprofile
    userProfile.seeAdminTools = False
    userProfile.save()
    return HttpResponse("done")

def randomQuestion(request):
    questionContainer = QuestionContainer.random()
    return recurseQuestionContainerDetail(request, questionContainer)

def massEditTags(request,question_pk):
    tags = Tag.objects.all()
    for tag in tags:
        # tag is checked
        if request.POST.get(tag.text,False):
            question = Question.objects.get(pk=question_pk)
            tag.questions.add(question)
        else:
            question = Question.objects.get(pk=question_pk)
            tag.questions.remove(question)
