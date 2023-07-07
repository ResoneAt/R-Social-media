# Generated by Django 4.2.2 on 2023-07-07 07:56

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_postmodel_image_delete_imagepostmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecyclePost',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('posts.postmodel',),
            managers=[
                ('deleted', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='postmodel',
            name='deleted_at',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='postmodel',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
