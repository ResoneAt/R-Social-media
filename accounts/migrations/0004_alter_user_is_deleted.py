# Generated by Django 4.2.2 on 2023-07-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_deleted_at_user_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False, editable=False, null=True),
        ),
    ]
