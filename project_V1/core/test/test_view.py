from django.test import TestCase,Client
from django.urls import reverse
from core.models import following,tweets_data,notification_data
from login.models import User_detail,Registration

class TestCoreViews(TestCase):
    def test_twitter_check_3(self):
       
        client=Client()
        response=client.post(reverse("twitter_check"))

        self.assertEquals(response.status_code,302)
        


    def test_followers_check1(self):
        client=Client()
        response=client.get(reverse("follower"))
        self.assertEquals(response.status_code,302)


    def test_follower_check2(self):
        client=Client()
        session=client.session
        session['username']="Akashsri"
        session.save()

        response=client.post(reverse("follower"),{
            "friend":"buddyupucd",
            "status":"Grant"
        })

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"followers.html")

    def test_follower_check3(self):
        client=Client()
        session=client.session
        session['username']="Akashsri"
        session.save()

        response=client.post(reverse("follower"),{
            "friend":"buddyupucd",
            "status":"Revoke"
        })

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"followers.html")
    
    def test_trend_check1(self):
        client=Client()
        response=client.get(reverse("trend"))
        self.assertEquals(response.status_code,302)    

    def test_trend_check2(self):
        following.objects.create(
            user_id="Akashsri",
            twitter_handle="buddyupucd",
            friend_Email="abc@gmail.com",
            url=",",
            isActive=1
        )
        client=Client()
        session=client.session
        session['username']="Akashsri"
        session.save()
        response=client.post(reverse("trend"),{
            "friend":"buddyupucd"
        })

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"trend.html")


    def test_trend_check3(self):
        
        client=Client()
        session=client.session
        session['username']="Akashsri"
        session.save()
        response=client.post(reverse("trend"))

        self.assertEquals(response.status_code,302)
        #self.assertTemplateUsed(response,"trend.html")




    def test_addfriend(self):
        client=Client()
        session=client.session
        session['username']="Akashsrivastava6"
        session.save()
        following.objects.create(
            user_id=session['username'],
            twitter_handle="buddyupucd",
            friend_Email="Akashsrivastava6@gmail.com",
            url="",
            isActive=1
        )
        response=client.post(reverse("addfriend"),{
            "twitter_handle":"buddyupucd",
            "email":"Akashsrivastava6@gmail.com"})

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"dashboard.html")


    def test_addfriend_without_session(self):
        client=Client()
       
        response=client.post(reverse("addfriend"),{
            "twitter_handle":"buddyupucd",
            "email":"Akashsrivastava6@gmail.com"})

        self.assertEquals(response.status_code,302)
        #self.assertTemplateUsed(response,"login")


    def test_twitter_check(self):
        User_detail.objects.create(
            username="Akashsrivastava6",
        )
        client=Client()
        session=client.session
        session['username']="Akashsrivastava6"
        session.save()
        response=client.post(reverse("twitter_check"),{
            "username":"Akashsrivastava6@gmail.com",
            "password":"Akashsri",
            "fname":"Akash",
            "lname":"Srivastava",
            "dob":"1992-03-03"
        })

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"dashboard.html")



    def test_twitter_check_1(self):
        User_detail.objects.create(
            username="Akashsrivastava6",
        )
        following.objects.create(
            user_id="Akashsrivastava",
            twitter_handle="Akashsrivastava6",
            friend_Email="abs@gmail.com",
            url="",
            isActive=1
        )
        client=Client()
        session=client.session
        session['username']="Akashsrivastava6"
        session.save()
        response=client.post(reverse("twitter_check"),{
            "username":"Akashsrivastava6@gmail.com",
            "password":"Akashsri",
            "fname":"Akash",
            "lname":"Srivastava",
            "dob":"1992-03-03"
        })

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"dashboard.html")   

    # def test_twitter_check_2(self):
       
    #     client=Client()
    #     session=client.session
    #     session['username']="Akashsrivastava6"
    #     session.save()
    #     response=client.post(reverse("twitter_check"),{
    #         "username":"Akashsrivast@gmail.com",
    #         "password":"Akashsri",
    #         "fname":"Akash",
    #         "lname":"Srivastava",
    #         "dob":"1992-03-04"
    #     })

    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response,"dashboard.html")   


   

        