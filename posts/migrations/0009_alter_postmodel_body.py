# Generated by Django 4.2.2 on 2023-10-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_postmodel_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='body',
            field=models.TextField(help_text='Please write caption'),
        ),
    ]
