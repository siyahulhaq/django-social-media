# Generated by Django 3.1.5 on 2021-03-14 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_auto_20210314_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='tweet',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tweets.tweet'),
        ),
    ]
