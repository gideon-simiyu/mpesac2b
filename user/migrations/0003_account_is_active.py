# Generated by Django 5.1.1 on 2024-10-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_account_user_account_email_account_paybill_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
