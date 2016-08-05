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
