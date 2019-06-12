from django.db import models

# Create your models here.
class User_detail(models.Model):
    username=models.CharField('Username',max_length=40,primary_key=True)
    password=models.CharField('Password',max_length=300)


    def __str__(self):
        return self.username



class Registration(models.Model):
    username=models.ForeignKey(User_detail,on_delete=models.CASCADE)
    FirstName=models.CharField('Last_Name',max_length=20)
    LastName=models.CharField('Last_Name',max_length=20)
    dateOfBirth=models.DateField('DateOfBirth')



    def __str__(self):
        return self.username



