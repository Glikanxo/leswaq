# Generated by Django 2.2 on 2022-02-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20220217_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annonce',
            name='images',
            field=models.ManyToManyField(to='core.PostImages'),
        ),
    ]
