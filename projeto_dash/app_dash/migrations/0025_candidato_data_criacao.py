# Generated by Django 4.2.3 on 2023-07-29 17:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_dash', '0024_userprofile_alter_candidato_user_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
