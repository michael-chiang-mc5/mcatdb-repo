from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from UserProfile.models import UserProfile
from UserProfile.views import new_user
from .models import *
from django.core.urlresolvers import reverse

def index(request):
    return HttpResponseRedirect(reverse('myContent:questionOfTheDay'))

# front page of mcatDB. Displays a random "Question of the Day"
def questionOfTheDay(request):
    if request.user.is_authenticated():
        userProfileExists = UserProfile.exists(request.user)
        if not userProfileExists:
            user = request.user
            userprofile = UserProfile(user=user,alias=user.username)
            userprofile.save()

    questionOfTheDay = QuestionOfTheDay.get_questionOfTheDay()
    try:
        questionContainer = questionOfTheDay.questionContainer # if no questionsOfTheDay, questionOfTheDay = None
    except:
        return render(request,'Test/questionContainerList.html')

    comments = questionContainer.comment_set.order_by('time')
    if questionContainer.type() == "question":
        context = {'questionContainer':questionContainer,'question':questionContainer.content_object,'comments':comments,'showComments':'0','frontpage':True}
        return render(request, 'Test/questionContainerDetail.html', context)
    elif questionContainer.type() == "passage":
        context = {'questionContainer':questionContainer,'passage':questionContainer.content_object,'comments':comments,'showComments':'0','frontpage':True}
        return render(request, 'Test/questionContainerDetail.html', context)

def about(request):
    return render(request,'myContent/about.html')

def admin_questionOfTheDay(request):
    if not request.user.is_superuser:
        return HttpResponse("You do not have permission")
    questionsOfTheDay = QuestionOfTheDay.objects.order_by('order')
    context = {'questionsOfTheDay':questionsOfTheDay}
    return render(request, 'myContent/admin_questionOfTheDay.html', context)

def adminOptions_questionOfTheDay(request):
    addOrRemove =request.POST.get('addOrRemove')
    questionContainer_pk = request.POST.get('questionContainer_pk')
    order       = request.POST.get('order')
    if order == '':
        order = QuestionOfTheDay.max_order() + 1

    if addOrRemove == 'add':
        questionOfTheDay = QuestionOfTheDay(questionContainer=QuestionContainer.objects.get(pk=questionContainer_pk),order=order)
        questionOfTheDay.save()
    if addOrRemove == 'remove':
        questionsOfTheDay = QuestionOfTheDay.objects.filter(questionContainer=questionContainer_pk)
        questionsOfTheDay.delete()

    return HttpResponseRedirect(reverse('myContent:admin_questionOfTheDay'))
