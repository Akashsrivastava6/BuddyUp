# Generated by Django 2.2.1 on 2019-06-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20190607_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_detail',
            name='username',
            field=models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Username'),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20, verbose_name='First_Name')),
                ('lastName', models.CharField(max_length=20, verbose_name='Last_Name')),
                ('dateOfBirth', models.DateField(verbose_name='DateOfBirth')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User_detail')),
            ],
        ),
    ]