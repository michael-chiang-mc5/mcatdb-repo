from django.db import models
import random

class Passage(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    adminNotes = models.TextField()
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text
    def get_random_passage_pk():
        random_passage = Passage.objects.order_by('?').first()
        return random_passage.pk

# Question includes both passage-based questions and standalone questions
class Question(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    hidden = models.BooleanField(default=True)
    passage = models.ForeignKey(Passage, blank=True, null=True) # null if a standalone question
    notes = models.TextField(blank=True, null=True)
    adminNotes = models.TextField()
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text
    def get_random_standalone_question_pk():
        random_standalone_question = Question.objects.exclude(passage__isnull=False).order_by('?').first()
        return random_standalone_question.pk
    def get_random_passage_or_standaloneQuestion():
        num_passages = len(Passage.objects.all())
        num_standaloneQuestions = len(Question.objects.exclude(passage__isnull=False))
        random_integer = random.randint(0,num_passages+num_standaloneQuestions)
        if random_integer < num_passages:
            return 'passage'
        else:
            return 'standaloneQuestion'
    def is_standalone(self):
        if self.passage == None:
            return True

class Answer(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    question = models.ForeignKey(Question)
    correct = models.BooleanField(default=False)
    explanation = models.TextField()
    def __str__(self):
        return self.text

class Tag(models.Model):
    text = models.CharField(max_length=255, unique=True)
    questions  = models.ManyToManyField(Question, blank=True, related_name="tags")  # to access tags from Question instance, question.tags.all()
    def __str__(self):
        return self.text
    # saves a new class object if one does not already exist
    def newTag(text):
        tags = Tag.objects.filter(text=text)
        if len(tags)==0:
            tag = Tag(text=text)
            tag.save()
