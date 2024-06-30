# Generated by Django 4.2.11 on 2024-06-30 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_denuncia_aceptaresponsabilidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denunciado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comercio', models.CharField(blank=True, max_length=100, null=True)),
                ('denuncia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.denuncia')),
                ('denunciado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.vecino')),
            ],
        ),
        migrations.DeleteModel(
            name='DenunciadoReclamo',
        ),
    ]
