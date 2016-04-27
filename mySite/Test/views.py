from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
from MCEditor.views import editor
from MCBase.views import *

def submitPassageAnswers(request):
    for key in request.POST:
        if key[:8] == 'question':
            value = request.POST[key]

            return HttpResponse(value)

    user = request.user
    tags = Tag.objects.all()
    for tag in tags:
        # Tag was checkmarked (either include or exclude)
        if request.POST.get(tag.text,False):
            if request.POST.get(tag.text) == "include":
                user.userprofile.tags_include.add(tag)
                user.userprofile.tags_exclude.remove(tag)
            elif request.POST.get(tag.text) == "exclude":
                user.userprofile.tags_include.remove(tag)
                user.userprofile.tags_exclude.add(tag)
        # No tag checkmark
        else:
            user.userprofile.tags_include.remove(tag)
            user.userprofile.tags_exclude.remove(tag)
    return HttpResponse("finished")


# This displays a list of all truncated passages
def passageList(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    passages = Passage.objects.all()
    context = {'passages':passages}
    return render(request, 'Test/passageList.html', context)
# This displays a single passage with associated questions/answers
def passageDetail(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    passage = Passage.objects.get(pk=passage_pk)
    questions = passage.question_set.all()
    context = {'passage':passage,'questions':questions}
    return render(request, 'Test/passageDetail.html', context)

def standaloneQuestionList(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    questions = Question.objects.exclude(passage__isnull=False)
    context = {'questions':questions}
    return render(request, 'Test/questionList.html', context)
def questionDetail(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    question = Question.objects.get(pk=question_pk)
    answers = Answer.objects.filter(question=question)
    try:
        passage = question.passage
    except:
        passage = None;
    tags = question.tags.all()
    context = {'passage':passage, 'question':question, 'answers':answers, 'tags':tags}
    return render(request, 'Test/questionDetail.html', context)
def questionUserView(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    question = Question.objects.get(pk=question_pk)
    passage = question.passage
    context = {'passage':passage,'question':question}
    return render(request, 'Test/questionUserView.html', context)

def adminPanel(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    context = {}
    return render(request, 'Test/adminPanel.html', context)
def adminList(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")

    tags = Tag.objects.all()

    context = {'tags':tags}
    return render(request, 'Test/adminList.html', context)

# Methods to add and edit passages
def addPassageEditor(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:addPassage')
    form_data = {}
    header = "Add a passage"
    initial_text = ""
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def addPassage(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    form_text = request.POST.get("form-text")
    passage = Passage(text=form_text)
    passage.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[passage.pk]) )
def editPassageEditor(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editPassage',args=[passage_pk])
    form_data = {}
    header = "Edit a passage"
    # get initial text
    passage = Passage.objects.get(pk=passage_pk)
    initial_text = passage.text
    # return editor
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editPassage(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    form_text = request.POST.get("form-text")
    passage = Passage.objects.get(pk=passage_pk)
    passage.text = form_text
    passage.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[passage_pk]) )

# Methods to add and edit questions
def addQuestionEditor(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:addQuestion')
    form_data = serialize_json({'passage_pk':passage_pk,})
    header = "Add a question"
    initial_text = ""
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def addQuestion(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get question text
    form_text = request.POST.get("form-text")
    question = Question(text=form_text)
    # get passage corresponding to question
    serialized_form_data = request.POST.get("serialized-form-data")
    form_data = deserialize_json_string(serialized_form_data)
    passage_pk = int(form_data["passage_pk"])
    if passage_pk != 0:
        question.passage = Passage.objects.get(pk=passage_pk)
    # save
    question.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[passage_pk]) )
def editQuestionEditor(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editQuestion',args=[question_pk])
    form_data = {}
    header = "Edit a question"
    # get initial text
    question = Question.objects.get(pk=question_pk)
    initial_text = question.text
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editQuestion(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get question text
    form_text = request.POST.get("form-text")
    question = Question.objects.get(pk=question_pk)
    question.text=form_text
    # save
    question.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[question.passage.pk]) )

# Methods to add and edit answers
def addAnswerEditor(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:addAnswer')
    form_data = serialize_json({'question_pk':question_pk,})
    header = "Add an answer"
    initial_text = ""
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def addAnswer(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get answer text
    form_text = request.POST.get("form-text")
    answer = Answer(text=form_text)
    # get attached question
    serialized_form_data = request.POST.get("serialized-form-data")
    form_data = deserialize_json_string(serialized_form_data)
    question_pk = int(form_data["question_pk"])
    answer.question = Question.objects.get(pk=question_pk)
    # save
    answer.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[answer.question.passage.pk]) )
def deleteAnswer(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    answer = Answer.objects.get(pk=answer_pk)
    passage_pk = answer.question.passage.pk
    answer.delete()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[passage_pk]) )
def deleteQuestion(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    question = Question.objects.get(pk=question_pk)
    passage_pk = question.passage.pk
    question.delete()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[passage_pk]) )
def deletePassage(request,passage_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    passage = Passage.objects.get(pk=passage_pk)
    passage.delete()
    return HttpResponseRedirect( reverse('Test:passageList') )


def editAnswerEditor(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editAnswer',args=[answer_pk])
    form_data = {}
    header = "Edit an answer"
    # get initial text
    answer = Answer.objects.get(pk=answer_pk)
    initial_text = answer.text
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editAnswer(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get answer text
    form_text = request.POST.get("form-text")
    answer = Answer.objects.get(pk=answer_pk)
    answer.text = form_text
    # save
    answer.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[answer.question.passage.pk]) )
def editExplanationEditor(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    submit_url = reverse('Test:editExplanation',args=[answer_pk])
    form_data = {}
    header = "Edit an explanation"
    # get initial text
    answer = Answer.objects.get(pk=answer_pk)
    initial_text = answer.explanation
    # return html
    html = editor(request,submit_url,form_data,header,initial_text) # See MCEditor.views
    return html
def editExplanation(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    # get answer text
    form_text = request.POST.get("form-text")
    answer = Answer.objects.get(pk=answer_pk)
    answer.explanation = form_text
    # save
    answer.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[answer.question.passage.pk]) )


def markAnswerCorrect(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    answer = Answer.objects.get(pk=answer_pk)
    answer.correct = True
    answer.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[answer.question.passage.pk]) )
def markAnswerIncorrect(request,answer_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    answer = Answer.objects.get(pk=answer_pk)
    answer.correct = False
    answer.save()
    return HttpResponseRedirect( reverse('Test:passageDetail',args=[answer.question.passage.pk]) )

def addTag(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    text = request.POST.get("tag-text")
    Tag.newTag(text)
    tag = Tag.objects.get(text=text)
    question = Question.objects.get(pk=question_pk)
    tag.questions.add(question)
    return editTags(request,question_pk)
def removeTag(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    text = request.POST.get("tag-text")
    tag = Tag.objects.get(text=text)
    question = Question.objects.get(pk=question_pk)
    tag.questions.remove(question)
    tag.save()
    return editTags(request,question_pk)
def editTags(request,question_pk):
    if not request.user.is_superuser:
        return HttpResponse("You are not a superuser")
    question = Question.objects.get(pk=question_pk)
    tags = question.tags.all()
    allTags = Tag.objects.all()
    context = {'question':question, 'tags':tags, 'allTags':allTags}
    return render(request, 'Test/editTags.html', context)
