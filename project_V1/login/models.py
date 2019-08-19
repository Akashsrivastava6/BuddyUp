from django.db import models
from datetime import datetime,timezone

# Create your models here.
# model for user_detail table
class User_detail(models.Model):
    username=models.CharField('Username',max_length=60,primary_key=True)
    password=models.CharField('Password',max_length=300)
    email=models.CharField('email',max_length=60,null=True)
    last_login=models.DateTimeField('last_login', default= datetime.now(timezone.utc))
    

    

# model for registration table
class Registration(models.Model):
    username=models.ForeignKey(User_detail,on_delete=models.CASCADE,primary_key=True) 
    FirstName=models.CharField('First_Name',max_length=20)
    LastName=models.CharField('Last_Name',max_length=20)
    dateOfBirth=models.DateField('DateOfBirth')



    



