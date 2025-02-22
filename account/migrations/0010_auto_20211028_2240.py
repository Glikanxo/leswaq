# Generated by Django 2.2 on 2021-10-28 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20211026_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mode',
            field=models.CharField(choices=[('aucun', 'Aucun'), ('secure', 'Sécurisé'), ('online_seller', 'Vendeur en ligne'), ('kid', 'Enfant'), ('ado', 'Adolescent'), ('entreprise', 'Entreprise'), ('special_needs', 'Besoins spéciaux')], default='aucun', max_length=30),
        ),
    ]
