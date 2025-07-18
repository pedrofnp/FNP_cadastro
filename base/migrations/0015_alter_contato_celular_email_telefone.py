# Generated by Django 5.1.2 on 2024-10-23 22:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_partido_contato_entidade_contato_partido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contato',
            name='celular',
            field=models.EmailField(max_length=254),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.EmailField(max_length=254)),
                ('contato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='base.contato')),
            ],
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=15)),
                ('contato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to='base.contato')),
            ],
        ),
    ]
