# Generated by Django 4.2.3 on 2023-07-23 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dash', '0013_remove_vaga_empresa_delete_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_empresa', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=14)),
            ],
        ),
    ]
