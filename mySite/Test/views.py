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
from .views_comment import *

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
    if request.user.is_authenticated():
        questionContainer = QuestionContainer.random(request.user)
        return recurseQuestionContainerDetail(request, questionContainer)
    else:
        return HttpResponse("You must log in (go back and look at top right hand corner)")
