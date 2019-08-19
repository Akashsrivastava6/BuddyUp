from django.db import models

# Create your models here.
# model for following table
class following(models.Model):
    class Meta:
        unique_together=(("user_id","twitter_handle"),)
    user_id=models.CharField("user_id",max_length=40)
    twitter_handle=models.CharField("twitter_handle",max_length=40,default="abc@abc.com")
    friend_Email=models.CharField("friend_Email", max_length=40)
    url=models.CharField("url",max_length=100,default="")
    isActive=models.BooleanField(default=False)

# model for tweets_data table
class tweets_data(models.Model):
    twitter_handle=models.CharField("twitter_handle",max_length=40)
    tweet_id=models.BigIntegerField("tweets_id",primary_key=True)
    tweet_data=models.TextField("tweet_data",max_length=1000)
    tweet_date=models.DateTimeField("date")
    is_notification=models.BooleanField(default=False)
    score=models.FloatField("score",default=0)
    sum_score=models.IntegerField("sum_score",default=0)
    counter=models.IntegerField("counter",default=0)
# model for notification_data table
class notification_data(models.Model):
    twitter_handle=models.CharField("twitter_handle",max_length=40)
    tweet_data=models.TextField("tweet_data",max_length=1000)
    noti_date=models.DateTimeField("noti_date")
    is_notified=models.BooleanField(default=False)