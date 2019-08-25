# BuddyUP 

An application which provides a platform that helps in passive well-being assessment of user’s loved ones. It tries to accomplish this task by constant monitoring oftweets and reporting a critical/notifiable tweet to the user.  This early reporting of critical tweets willhelp the end user to intervene and provide emotional support to his friend/family at the right time. 


## Technology Stack

- **Application Development**: Python
- **Web Framework**: Django
- **Persistent Database** - MySQL
- **UI/UX**: HTML/CSS/JavaScript
- **CSS Framework**: Bootstrap
- **Authentication Package**: SocialAuth Django
- **Scheduling**: Celery
- **Tweets Retrieval**: Tweepy
-  **Tweets Pre-processing**: Spacy, Pandas

## Important Files

There are two apps in the project, one is core and the other is login. 

### Core

Contains files which are important for acquiring the data and pushing it to the trend page in the form of JSON object. It is responsible for preprocessing the tweets and calculating their sentiment scores. 

### Login 

This application is responsible for the overall functionality of the dashboard of and contains all the static pages required to develop the UI of the application. 

### The main files in the application are: 

- Views.py: This is one of the most important files in the application as this contains callable classes which takes requests and then returns them as a response to the task.py file. 
- Task.py: Contains all the callable functions responsible for performing tasks in the application
- urls.py: This file is responsible 
- Processes.py: Contains all the functions to pre-process the tweets and the algorithm to calculate the sentiment score of the tweets
- Templates 
  - Homepage.html: This is the landing page of the applicaion and the main page as well
  - Dashboard.html: This is the main dashboard ozf user who registers to our application 
  - Login.html: Provides Login form for the application 
  - Signup.html: Provides Signup form for the application
  - Trend.html: This page is the trend page of the application and one can see the overall well-being trend in this page. 

- Static: This folder consists of all the stylesheets and images required to build the applicaiton. 

## Installing 

You need to install the required packages to begin with by using the code below:

```
pip install -r requirements.txt
```

To create the database for the application, migrations are needed which can be created by the following code: 

```
python manage.py makemigrations
```
Once the migrations are created, you need to migrate them using:
```
python manage.py migrate
```
Once the migrations are migrated, you can start the application by the following code:
```
python manage.py runserver
```

## Authors 

- **Arnab Tarwani** - [arnabtarwani](https://github.com/arnabtarwani)
- **Akash Srivastava** - [akashsrivastava](https://github.com/Akashsrivastava6)
- **Arpan Tiwari** - [arpantiwari](https://github.com/arpantiwari)
- **Arunuday Ganju** - [arunduayganju](https://github.com/ArunudayGanju)
- **Achin Tamiri** = [achintamiri](https://github.com/achintamiri)

## License 

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
