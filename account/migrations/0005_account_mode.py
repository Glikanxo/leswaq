# Generated by Django 2.2 on 2021-05-13 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mode',
            field=models.CharField(default='aucun', max_length=30),
        ),
    ]
