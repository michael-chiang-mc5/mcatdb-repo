from .models import *
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def addComment(request,questionContainer_pk):
    form_text = request.POST.get("form-text")
    comment = Comment(text=form_text,user=request.user,questionContainer=QuestionContainer.objects.get(pk=questionContainer_pk))
    comment.save()
    return HttpResponseRedirect(reverse('Test:questionContainerDetail', args=[questionContainer_pk]))
