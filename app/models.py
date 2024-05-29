from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Profile(User):
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="images", default="images/avatar_one.jpg")
    # user = models.OneToOneField(User, on_delete=models.PROTECT)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "%s"%(self.name)

class QuestionManager(models.Manager):
    def get_hot(self):
        # return self.filter(questionlike__gt=17)
        return self.annotate(num_likes=Count("questionlike__question")).order_by('-num_likes', 'created_at')
    def get_new(self):
        return self.order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = QuestionManager()
    

    def __str__(self):
        return "%s"%(self.title)
    

class AnswerManager(models.Manager):
    def get_order_by_answers(self):
        return self.annotate(num_likes=Count("answerlike")).order_by('-truth_checkbox', '-num_likes')
class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    truth_checkbox = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()



class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_answerlike_user')
        ]


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_questionlike_user')
        ]