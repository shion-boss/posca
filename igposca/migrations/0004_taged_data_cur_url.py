# Generated by Django 3.0.7 on 2020-11-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igposca', '0003_account_subscription_target_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='taged_data',
            name='cur_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]