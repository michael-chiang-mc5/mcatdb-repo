from django.shortcuts import render
from copy import deepcopy
from .models import *
from .views_detail import *

def adminPanel(request):
    #if not request.user.is_superuser: # TODO: add back in
    #    return HttpResponse("You are not a superuser")
    context = {}
    return render(request, 'Test/adminPanel.html', context)

# copy
def copyQuestionContainer(request,questionContainer_pk):
    questionContainer = QuestionContainer.objects.get(pk=questionContainer_pk)
    new_qC = questionContainer.deepcopy()
    return recurseQuestionContainerDetail(request, new_qC)

def copyQuestionInPassage(request,question_pk):
    question = Question.objects.get(pk=question_pk)
    new_question = question.deepcopy()
    passage = question.passages.all()[0]
    passage.questions.add(new_question)
    passage.save()
    return recurseQuestionContainerDetail(request, passage)
