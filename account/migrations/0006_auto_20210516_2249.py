# Generated by Django 2.2 on 2021-05-16 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_account_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='wilaya',
            field=models.CharField(choices=[('Adrar', 'Adrar'), ('Chlef', 'Chlef'), ('Laghouat', 'Laghouat'), ('Oum el bouaghi', 'Oum el bouaghi'), ('Batna', 'Batna'), ('Béjaïa', 'Bejaia'), ('Biskra', 'Biskra')], max_length=80),
        ),
    ]
