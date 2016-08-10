from .models import *
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from MCEditor.views import editor
from .views_detail import *

def addComment(request,questionContainer_pk):
    form_text = request.POST.get("form-text")
    reply_at = request.POST.get("reply_at")
    # comment is NOT a reply to another comment
    if reply_at == "None":
        comment = Comment(text=form_text,user=request.user,questionContainer=QuestionContainer.objects.get(pk=questionContainer_pk))
    # comment is a reply to another comment
    else:
        comment = Comment(text=form_text,user=request.user,questionContainer=QuestionContainer.objects.get(pk=questionContainer_pk),reply_at=Comment.objects.get(pk=reply_at))

    comment.save()
    return recurseQuestionContainerDetail_withComments(request,comment.questionContainer)

def editCommentEditor(request,comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.pk != comment.user.pk:
        return HttpResponse("You do not have permission to edit this comment")
    submit_url = reverse('Test:editComment',args=[comment_pk])
    form_data = {}
    header = "Edit your comment"
    # get initial text
    initial_text = comment.text
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editComment(request,comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.pk != comment.user.pk:
        return HttpResponse("You do not have permission to edit this comment")
    # get text
    form_text = request.POST.get("form-text")
    comment.text = form_text
    # save
    comment.save()
    return recurseQuestionContainerDetail_withComments(request,comment.questionContainer)

def deleteComment(request,comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.pk != comment.user.pk:
        return HttpResponse("You do not have permission to edit this comment")
    qC = comment.questionContainer
    comment.delete()
    return recurseQuestionContainerDetail_withComments(request,qC)
