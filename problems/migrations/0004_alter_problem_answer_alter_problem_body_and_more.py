# Generated by Django 4.2.19 on 2025-03-07 01:59

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_problem_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='answer',
            field=markdownx.models.MarkdownxField(),
        ),
        migrations.AlterField(
            model_name='problem',
            name='body',
            field=markdownx.models.MarkdownxField(),
        ),
        migrations.AlterField(
            model_name='problem',
            name='explanation',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
