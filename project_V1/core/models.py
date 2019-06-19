from django.db import models

# Create your models here.
class following(models.Model):
    class Meta:
        unique_together=(("user_id","friend_Email"),)
    user_id=models.CharField("user_id",max_length=40)
    twitter_handle=models.CharField("twitter_handle",max_length=40)
    friend_Email=models.CharField("friend_Email", max_length=40,default="abc@abc.com")
    url=models.CharField("url",max_length=100,default="")
    isActive=models.BooleanField(default=False)


class tweets_data(models.Model):
    twitter_handle=models.CharField("twitter_handle",max_length=40)
    tweet_id=models.BigIntegerField("tweets_id",primary_key=True)
    tweet_data=models.TextField("tweet_data",max_length=280)
    tweet_date=models.DateField("date")