from django.test import TestCase ,Client
from django.urls import reverse
from login.models import User_detail,Registration
from core.models import following,notification_data
from passlib.hash import pbkdf2_sha256

class Test_login_views(TestCase):
    def test_signup(self):
        client=Client()
        response=client.get(reverse("signup"))
        #print("inside login view test")
        self.assertEquals(response.status_code,200)

    def test_Registration(self):
        client=Client()
        response=client.post(reverse("register"),{
            "username":"akashsrivastava@gmail.com",
            "password":"Akashsri92",
            "fname":"Akash",
            "lname":"Srivastava",
            "dob":"2001-03-28"})

        self.assertEquals(response.status_code,200)
        self.assertEquals(Registration.objects.count(),1)
        self.assertEquals(User_detail.objects.count(),1)

    def test_login(self):
        pwd="Akashsri92"
        pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000)
        User_detail.objects.create(
            username="Akashsrivastava6@gmail.com",
            password=pwd,
            email="Akashsrivastava6@gmail.com"
        )


        client=Client()
        response=client.post("/login/submit",{
            "username":"Akashsrivastava6@gmail.com",
            "password":"Akashsri92"
        })  
        #print(response['location'])      
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"dashboard.html")

    def test_login_session(self):
        client=Client()
        session=client.session
        session['username']="Akashsrivastava6@gmail.com"
        session.save()
        response=client.post("/login/submit") 
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"dashboard.html")

    def test_login_wrong_password(self):
        pwd="Akashsri92"
        pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000)
        User_detail.objects.create(
            username="Akashsrivastava6@gmail.com",
            password=pwd,
            email="Akashsrivastava6@gmail.com"
        )

        following.objects.create(
            user_id="Akashsrivastava6@gmail.com",
            twitter_handle="buddyupucd",
            friend_Email="Akashsrivastava6@gmail.com",
            url="",
            isActive=1
        )
        notification_data.objects.create(
            twitter_handle="buddyupucd",
            tweet_data="test",
            noti_date="2019-07-29 11:59:12.000000"

        )



        client=Client()
        response=client.post("/login/submit",{
            "username":"Akashsrivastava6@gmail.com",
            "password":"Akashsri"
        })  
        #print(response['location'])      
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"index.html")

    def test_login_user_not_reg(self):
        

        client=Client()
        response=client.post("/login/submit",{
            "username":"Akashsrivastava6@gmail.com",
            "password":"Akashsri"
        })  
        #print(response['location'])      
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"index.html")





    def test_login_page_withsession(self):
        client=Client()
        session=client.session
        session['username']="Akashsrivastava6@gmail.com"
        session.save()
        response=client.post("/login/") 
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"dashboard.html")

    
    def test_login_page_withou_session(self):
        client=Client()
        response=client.post("/login/") 
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"index.html")
