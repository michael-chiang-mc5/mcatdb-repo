from .models import *
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Abstraction to display single Question or Passage using QuestionContainer interface
def recurseQuestionContainerDetail(request, obj):
    questionContainer_pk = obj.questionContainer_pk()
    return HttpResponseRedirect(reverse('Test:questionContainerDetail',args=[questionContainer_pk,0]))

# Abstraction to display single Question or Passage using QuestionContainer interface
def recurseQuestionContainerDetail_withComments(request, obj):
    questionContainer_pk = obj.questionContainer_pk()
    return HttpResponseRedirect(reverse('Test:questionContainerDetail',args=[questionContainer_pk,1]))

def questionContainerList(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    questionContainers = QuestionContainer.objects.all()
    for questionContainer in questionContainers:
        tags = Tag.objects.extra( select={'lower_text': 'lower(text)'}).order_by("lower_text").all() # tags sorted in alphabetical order
        questionContainer.taglist = tags
        for i,tag in enumerate(questionContainer.taglist):
            questionContainer.taglist[i].checked = tag in questionContainer.tags.all()
    context = {'questionContainers':questionContainers,'tagAdmin':True}
    return render(request, 'Test/questionContainerList.html', context)


def questionContainerDetail(request,questionContainer_pk,showComments):
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
    comments = questionContainer.comment_set.order_by('time')
    if questionContainer.type() == "question":
        context = {'questionContainer':questionContainer,'question':questionContainer.content_object,'comments':comments,'showComments':showComments}
        return render(request, 'Test/questionContainerDetail.html', context)
    elif questionContainer.type() == "passage":
        context = {'questionContainer':questionContainer,'passage':questionContainer.content_object,'comments':comments,'showComments':showComments}
        return render(request, 'Test/questionContainerDetail.html', context)
