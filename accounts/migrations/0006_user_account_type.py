# Generated by Django 4.2.2 on 2023-06-19 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_followrequestmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('public', 'Public'), ('privet', 'Privet')], default='public', max_length=10),
        ),
    ]
