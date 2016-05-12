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
    def get_random_passage_pk(user):
        # filter by include/exclude tags
        tags_include = user.userprofile.tags_include.all()
        tags_exclude = user.userprofile.tags_exclude.all()
        if len(tags_include) > 0:
            questions = Question.objects.filter(tags__in=tags_include)
        else:
            questions = Question.objects.all()
        questions = questions.exclude(tags__in=tags_exclude)
        # get filtered passages
        passages = Passage.objects.filter(question__in=questions).distinct()
        random_integer = random.randint(0,passages.count()-1)
        random_passage = passages[random_integer]
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
    def get_random_standalone_question_pk(user):
        # filter by include/exclude tags
        tags_include = user.userprofile.tags_include.all()
        tags_exclude = user.userprofile.tags_exclude.all()
        if len(tags_include) > 0:
            questions = Question.objects.filter(tags__in=tags_include)
        else:
            questions = Question.objects.all()
        questions = questions.exclude(tags__in=tags_exclude)
        # get standalone question
        questions = questions.exclude(passage__isnull=False)
        random_integer = random.randint(0,questions.count()-1)
        random_standalone_question = questions[random_integer]
        return random_standalone_question.pk
    # returns 'standaloneQuestion' if question is a standalone question, or 'passage' if question is part of a passage
    def get_random_passage_or_standaloneQuestion(user):
        # filter by include/exclude tags
        tags_include = user.userprofile.tags_include.all()
        tags_exclude = user.userprofile.tags_exclude.all()
        if len(tags_include) > 0:
            questions = Question.objects.filter(tags__in=tags_include)
        else:
            questions = Question.objects.all()
        questions = questions.exclude(tags__in=tags_exclude)
        # get number of passages / standalone questions
        num_passages = Passage.objects.filter(question__in=questions).distinct().count()
        num_standaloneQuestions = questions.exclude(passage__isnull=False).count()
        # randomly choose passage/standaloneQuestion
        random_integer = random.randint(0,num_passages+num_standaloneQuestions-1)
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
