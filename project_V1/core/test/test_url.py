from django.test import SimpleTestCase
from django.urls import reverse,resolve
from core.views import AddFriend,Checkingtwitter,Checking


class TestUrls(SimpleTestCase):
    
    def  test_login(self):
        url=reverse('login')
        # print(resolve(url))

        self.assertEquals(resolve(url).func,Checking)

    def test_addfriend(self):
        url=reverse('addfriend')
        # print(resolve(url))

        self.assertEquals(resolve(url).func,AddFriend)
    
    # def test_trend(self):
    #     url=reverse('trend')
    #     print(resolve(url))

    #     self.assertEquals(resolve(url).func,trend)


    
    # def test_followers(self):
    #     url=reverse('followers')
    #     print(resolve(url))

    #     self.assertEquals(resolve(url).func,Followers)

    
    def test_checking_twitter(self):
        url=reverse('twitter_check')
        # print(resolve(url))

        self.assertEquals(resolve(url).func,Checkingtwitter)     

    