# Generated by Django 4.2.16 on 2024-10-30 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_contato_emails_alter_email_contato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefone',
            name='contato',
        ),
        migrations.DeleteModel(
            name='Email',
        ),
        migrations.DeleteModel(
            name='Telefone',
        ),
    ]
