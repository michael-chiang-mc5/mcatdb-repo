from .models import *
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Abstraction to display single Question or Passage using QuestionContainer interface
def recurseQuestionContainerDetail(request, obj):
    questionContainer_pk = obj.questionContainer_pk()
    return questionContainerDetail(request,questionContainer_pk)

# display all questionContainers
def questionContainerList(request):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    questionContainers = QuestionContainer.objects.all()
    context = {'questionContainers':questionContainers}
    return render(request, 'Test/questionContainerList.html', context)

def questionContainerDetail(request,questionContainer_pk):
    #if not request.user.is_superuser:
    #    return HttpResponse("You are not a superuser")
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)

    comments = questionContainer.comment_set.all()

    if questionContainer.type() == "question":
        context = {'questionContainer':questionContainer,'question':questionContainer.content_object,'comments':comments}
        return render(request, 'Test/questionContainerDetail.html', context)
    elif questionContainer.type() == "passage":
        context = {'questionContainer':questionContainer,'passage':questionContainer.content_object,'comments':comments}
        return render(request, 'Test/questionContainerDetail.html', context)
