# Generated by Django 2.2.1 on 2019-06-10 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_registration_user_detail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Registration',
        ),
        migrations.DeleteModel(
            name='User_detail',
        ),
    ]
