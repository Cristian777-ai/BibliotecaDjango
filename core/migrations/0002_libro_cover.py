# Generated by Django 4.2.21 on 2025-05-20 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='cover',
            field=models.ImageField(blank=True, help_text='Portada del libro', null=True, upload_to='covers/'),
        ),
    ]
