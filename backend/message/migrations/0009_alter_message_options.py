# Generated by Django 4.2.4 on 2023-11-22 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0008_alter_message_reply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id']},
        ),
    ]