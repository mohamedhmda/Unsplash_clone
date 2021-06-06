# Generated by Django 3.2.3 on 2021-05-25 12:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_image_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='image',
            name='location',
            field=models.CharField(default=None, max_length=256),
        ),
        migrations.AddField(
            model_name='image',
            name='published_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date ordered'),
        ),
    ]
