from django.core.management.base import BaseCommand, CommandError, CommandParser
from app.models import Question
from app.models import Answer
from app.models import Tag
from app.models import Status

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
        #добавить еще статус
        status = [Status(like_count=((i % 3)*10 + 3)) for i in range(1, ratio*110 + 1)]
        print('list status')
        Status.objects.bulk_create(status)
        print('status')
        tags = [Tag(name=f'Тег номер {i}') for i in range(ratio)]
        print('list tag')
        Tag.objects.bulk_create(tags)
        print('tags') 
        
        questions = [Question(title=f'Вопрос номер {i}', text=f'Текст вопроса номер {i}', status_id= i) for i in range(1, ratio*10 + 1)]
        Question.objects.bulk_create(questions)
        print('questions')

           
        #блок ответов
        # statuses2 = [Status(like_count=((i % 3)*10 + 3)) for i in range(ratio*10 + 1, ratio*110 + 1)]
        print('start')
        answers = [Answer(title=f'Ответ номер {i}', text=f'Текст ответа номер {i}', status_id= i + ratio*10, truth_checkbox=False, question_id = ((i - 1) // 10) + 1) for i in range(1, ratio*100 + 1)]
        print('list answer')
        Answer.objects.bulk_create(answers)
        print('answers')
            
        


