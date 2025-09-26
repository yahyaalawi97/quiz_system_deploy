from django.db import models
import re
from django.utils import timezone

class LOGINManeger (models.Manager):
    def basic_validator(Self , postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "the first name must be atleast 2 charcters"
        if len(postData["last_name"]) <2:
            errors["last_name"] = "the last name must be at leaset 2 charcters"
        if len(postData["password"])<5:
            errors["password"]="the password should be atleast 5 charcters"
        if postData["password"] != postData["confirm_password"]:
            errors["password"]="the passwords must be matched"
        if not EMAIL_REGEX.match(postData["email"]):
            errors['email']="invalid email !"
        from .models import User  
        if User.objects.filter(email=postData.get("email")).exists():
            errors["email_exists"] = "This email is already registered!"
        return errors

class User(models.Model):
    role_choice = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices = role_choice, default='student') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LOGINManeger()
    def __str__(self):
        return f" {self.first_name} : {self.role} "

class QuizManeger (models.Manager):
    def quiz_validator(Self , postData):
        errors = {}
        if len(postData["title"]) < 3:
            errors["title"] = "the title for quiz must be atleast 3 charcters"
        if len(postData["desc"]) < 10:
            errors["desc"] = "the desccription for quiz must be atleast 10 charcters"
        return errors

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User , related_name="quiz_maker",on_delete=models.CASCADE ,null=True) 
    objects = QuizManeger()
    def __str__(self):
        return f"{self.title}"

class QuestionManeger (models.Manager):
    def question_validator(Self , postData):
        errors = {}
        if len(postData["question_text"]) < 3:
            errors["title"] = "the question text must be at least 3 charcters"
        if postData.get("question_type") == 'mcq':
            options = postData.get("options", [])
            if not options or len(options) < 2:
                errors["options"] = "MCQ questions must be at least 2 options."
            correct = postData.get("correct_answer", "")
            if correct not in options:
                errors["correct_answer"] = "Correct answer must be one of the options."
        return errors

class Question(models.Model):
   question_type = (
        ('mcq', 'Multiple Choice'),
        ('tf', 'True/False'),
    )   
   quiz = models.ForeignKey(Quiz , related_name="questions" , on_delete=models.CASCADE)
   question_text = models.TextField()
   question_type = models.CharField(max_length=10, choices=question_type, default='mcq')
   options = models.JSONField(blank=True, null=True) 
   correct_answer = models.CharField(max_length=255)
   objects = QuestionManeger()

   def __str__(self):
        return f"Q: {self.question_text[:50]}..."
   
class ResultManager(models.Manager):
    def result_validator(self, postData, quiz):
        errors = {}
        score = postData.get("score")
        try:
            score = int(score)
        except (ValueError, TypeError):
            errors["score"] = "Score must be a number."
            return errors
        total_questions = quiz.questions.count()
        if score < 0:
            errors["score"] = "Score cannot be negative."
        elif score > total_questions:
            errors["score"] = f"Score cannot exceed total questions ({total_questions})."

        return errors

   
class result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField()
    attempt_date = models.DateTimeField(default=timezone.now)
    objects = ResultManager()

    def __str__(self):
        return f"{self.user.first_name} - {self.quiz.title} ({self.score})"
# Create your models here.
