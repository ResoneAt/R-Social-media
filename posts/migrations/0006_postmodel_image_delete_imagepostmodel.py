# Generated by Django 4.2.2 on 2023-07-06 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_postmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='image',
            field=models.ImageField(blank=True, help_text='Please upload your image', null=True, upload_to='posts'),
        ),
        migrations.DeleteModel(
            name='ImagePostModel',
        ),
    ]