# Generated by Django 4.2.3 on 2023-07-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dash', '0005_rename_usuario_perfilusuario_alter_vaga_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]