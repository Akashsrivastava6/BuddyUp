# Generated by Django 2.2.1 on 2019-06-11 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20190611_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='username',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='login.User_detail', unique=True),
        ),
    ]
