# Generated by Django 2.2.1 on 2019-06-09 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20190607_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='firstName',
        ),
    ]
