# Generated by Django 4.2.16 on 2024-12-03 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_review_reviewcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
