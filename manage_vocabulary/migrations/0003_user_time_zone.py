# Generated by Django 4.2.2 on 2023-07-03 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_vocabulary', '0002_word_added_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time_zone',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
