# Generated by Django 5.0.6 on 2024-05-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_superadmin_token_nobox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superadmin',
            name='token_nobox',
        ),
        migrations.AddField(
            model_name='adminsekolah',
            name='token_nobox',
            field=models.TextField(blank=True, null=True),
        ),
    ]