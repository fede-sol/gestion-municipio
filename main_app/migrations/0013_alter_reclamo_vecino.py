# Generated by Django 4.2.11 on 2024-06-30 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_personal_categoria_alter_promocion_rubro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamo',
            name='vecino',
            field=models.ForeignKey(blank=True, db_column='documento', null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.vecino'),
        ),
    ]
