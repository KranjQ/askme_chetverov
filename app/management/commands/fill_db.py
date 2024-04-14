from django.core.management.base import BaseCommand, CommandError, CommandParser
from app.models import Question
from app.models import Answer
from app.models import Tag
# from app.models import Status
from app.models import AnswerLike
from app.models import QuestionLike
from django.contrib.auth.models import User

# class Question(models.Model):
#     title = models.CharField(max_length=255)
#     text = models.CharField(max_length=1024)
#     status = models.ForeignKey(Status, on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Answer(models.Model):
#     title = models.CharField(max_length=255)
#     text = models.CharField(max_length=1024)
#     status = models.ForeignKey(Status, on_delete=models.CASCADE)
#     truth_checkbox = models.BooleanField()
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Status(models.Model):
#     like_count = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Profile(models.Model):
#     avatar = models.ImageField(null=True, blank=True)
#     user = models.OneToOneField(User, on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Tag(models.Model):
#     name = models.CharField(max_length=255)
#     question = models.ManyToManyField(Question)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        print(ratio)
        
        users = [User.objects.create_user(f"User {i}", f"{i}_user@gmail.com", f"{i}_user_password") for i in range(1, ratio + 1)]
        

        print("end user block")
            

        tags = [Tag(name=f'Тег номер {i}') for i in range(ratio)]
        print('created list tag')
        Tag.objects.bulk_create(tags)
        print('saved in db tags') 
        
        questions = [Question(title=f'Вопрос номер {i}', text=f'Текст вопроса номер {i}') for i in range(1, ratio*10 + 1)]
        Question.objects.bulk_create(questions)
        print('created questions')

        for question in questions:
            for i in range(6):
                question.tags.add(tags[(i * question.id) % ratio])
            answers = [Answer(title=f'Ответ номер {i}', text=f'Текст ответа номер {i}', truth_checkbox=False, question_id = question.id) for i in range(1, 11)]
            Answer.objects.bulk_create(answers)
            for answer in answers:
                answerLike = [AnswerLike(user_id = i, answer_id = answer.id) for i in range(1, ratio + 1)]
                AnswerLike.objects.bulk_create(answerLike)
            questionLike = [QuestionLike(user_id = i, question_id = question.id) for i in range(1, ratio + 1)]
            QuestionLike.objects.bulk_create(questionLike)


        # print('start')
        # answers = [Answer(title=f'Ответ номер {i}', text=f'Текст ответа номер {i}', truth_checkbox=False, question_id = ((i - 1) // 10) + 1) for i in range(1, ratio*100 + 1)]
        # print('list answer')
        # Answer.objects.bulk_create(answers)
        # print('answers')
        

        # answerLike = [AnswerLike(like_count=((i % 3)*10 + 3), user_id = (i % ratio), answer_id = (i % ratio*100)) for i in range(1, ratio*100 + 1)]
        # AnswerLike.objects.bulk_create(answerLike)
        # print('answerLike')

        # questionLike = [QuestionLike(like_count=((i % 3)*10 + 3), user_id = (i % ratio), question_id = (i % ratio*10)) for i in range(1, ratio*10 + 1)]
        # QuestionLike.objects.bulk_create(questionLike)
        # print('questionLike')
        


