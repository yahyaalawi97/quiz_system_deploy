from django.db import models
import re

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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LOGINManeger()
# Create your models here.
