# Generated by Django 5.0.6 on 2024-07-25 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OpenAI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generatedimage',
            name='number_of_room_designs',
        ),
    ]