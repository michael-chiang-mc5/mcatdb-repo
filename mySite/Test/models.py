from django.db import models
import random
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Tag(models.Model):
    text = models.CharField(max_length=255, unique=True)
    priority = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return self.text
    # saves a new class object if one does not already exist
    @classmethod
    def newTag(self,text):
        tags = Tag.objects.filter(text=text)
        if len(tags)==0:
            tag = Tag(text=text)
            tag.save()

# all SingleQuestion and Passage objects link to a QuestionContainer object
# need to set content_object
class QuestionContainer(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    tags  = models.ManyToManyField(Tag, blank=True, related_name="questionContainers")  # to access questionContainers from tag instance, tag.questionContainers.all()
    # implements generic foreign key to passage and question objects
    # constructor: questionContainer = QuestionContainer(content_object=passage)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') # To get singleQuestion or passage object, questionContainer.content_object
    hidden = models.BooleanField(default=False)

    # random QuestionContainer object
    @staticmethod
    def random(user):
        # filter by include/exclude tags
        tags_include = user.userprofile.tags_include.all()
        tags_exclude = user.userprofile.tags_exclude.all()
        if len(tags_include) > 0:
            questionContainers = QuestionContainer.objects.all()
            for tag_include in tags_include:
                questionContainers = questionContainers.filter(tags__in=[tag_include])
        else:
            questionContainers = QuestionContainer.objects.all()
        questionContainers = questionContainers.exclude(tags__in=tags_exclude)
        # filter by question creation date
        if user.userprofile.mindate is None:
            mindate = datetime.datetime.min
        else:
            mindate = user.userprofile.mindate
        if user.userprofile.maxdate is None:
            maxdate = datetime.datetime.max
        else:
            maxdate = user.userprofile.maxdate
        questionContainers = questionContainers.filter(time__range=[mindate, maxdate])
        num = questionContainers.count()
        r = random.randint(0,num-1)
        return questionContainers[r]
    def questionContainer_pk(self):
        return self.pk
    def type(self):
        return self.content_object.type()
    def deepcopy(self):
        new_obj = self.content_object.deepcopy()
        new_qC = QuestionContainer(hidden=self.hidden,content_object=new_obj)
        new_qC.save() # saving is necessary to initialize ManyToManyField
        for tag in self.tags.all():
            new_qC.tags.add(tag)
        new_qC.save()
        return new_qC


class Answer(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    explanation = models.TextField()
    correct = models.BooleanField(default=False)
    adminNotes = models.TextField()
    def __str__(self):
        return self.text
    def editAdminNotes(self,text):
        self.adminNotes = text
    def question_pk(self):
        return self.questions.all()[0].pk
    def questionContainer_pk(self):
        question = self.questions.all()[0]
        return question.questionContainer_pk()
    def deepcopy(self):
        new_answer = Answer(text=self.text,explanation=self.explanation,correct=self.correct,adminNotes=self.adminNotes)
        new_answer.save()
        return new_answer


# Question can be part of a passage, or it can be a single question
class Question(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    adminNotes = models.TextField()
    answers  = models.ManyToManyField(Answer, blank=True, related_name="questions")  # to access questions from answer instance, answer.questions.all()
    questionContainer = GenericRelation(QuestionContainer)

    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text
    def editAdminNotes(self,text):
        self.adminNotes = text
    # Returns True if at least one of the answers corresponding to question has an explanation
    def hasExplanation(self):
        answers = self.answers.all()
        hasExplanation = False
        for answer in answers:
            if len(answer.explanation) > 0: # TODO: make a method
                hasExplanation = True
        return hasExplanation
    def type(self):
        return "question"
    # return the pk of encapsulating questionContainer
    def questionContainer_pk(self):
        if len(self.passages.all()) > 0:
            passage = self.passages.all()[0]
            questionContainer = passage.questionContainer.all()[0]
            return questionContainer.pk
        else: # single question
            questionContainer = self.questionContainer.all()[0]
            return questionContainer.pk
    def deepcopy(self):
        new_question = Question(text=self.text,adminNotes=self.adminNotes)
        new_question.save() # saving is necessary to initialize ManyToManyField
        for answer in self.answers.all():
            new_answer = answer.deepcopy()
            new_question.answers.add(new_answer)
        new_question.save()
        return new_question
    def is_passage(self):
        if len(self.passages.all()) > 0:
            return True
        return False

class Passage(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    adminNotes = models.TextField()
    questions  = models.ManyToManyField(Question, blank=True, related_name="passages")  # to access passages from question instance, question.passages.all()
    questionContainer = GenericRelation(QuestionContainer)

    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text
    def editAdminNotes(self,text):
        self.adminNotes = text
    def type(self):
        return "passage"
    def questionContainer_pk(self):
        return self.questionContainer.all()[0].pk
    def deepcopy(self):
        new_passage = Passage(text=self.text,adminNotes=self.adminNotes)
        new_passage.save() # saving is necessary to initialize ManyToManyField
        for question in self.questions.all():
            new_question = question.deepcopy()
            new_passage.questions.add(new_question)
        new_passage.save()
        return new_passage

class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User)
    reply_at = models.ForeignKey('self', blank=True, null=True)
    questionContainer = models.ForeignKey(QuestionContainer)
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text
    def is_reply(self):
        if self.reply_at is None:
            return False
        else:
            return True
