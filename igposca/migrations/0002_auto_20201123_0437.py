# Generated by Django 3.0.7 on 2020-11-22 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igposca', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taged_data',
            name='text',
            field=models.TextField(max_length=140),
        ),
    ]
