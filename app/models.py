from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Status(models.Model):
    like_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionManager(models.Manager):
    def get_hot(self):
        return self.filter(status__like_count__gt=20)
    def get_new(self):
        return self.order_by('-created_at').values()


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    # tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = QuestionManager()
    
class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    truth_checkbox = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    question = models.ManyToManyField(Question)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)