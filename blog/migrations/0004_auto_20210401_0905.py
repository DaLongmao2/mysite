# Generated by Django 3.1 on 2021-04-01 09:05

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210401_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
