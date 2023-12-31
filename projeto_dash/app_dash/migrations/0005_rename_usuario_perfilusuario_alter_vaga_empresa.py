# Generated by Django 4.2.3 on 2023-07-20 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_dash', '0004_candidato_empresa_usuario_vaga_delete_joblist_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usuario',
            new_name='PerfilUsuario',
        ),
        migrations.AlterField(
            model_name='vaga',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vagas', to='app_dash.empresa'),
        ),
    ]
