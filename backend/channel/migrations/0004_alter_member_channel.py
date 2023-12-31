# Generated by Django 4.2.4 on 2023-09-25 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_alter_member_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='channel.channel'),
        ),
    ]
