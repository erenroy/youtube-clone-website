# Generated by Django 4.1.3 on 2023-11-16 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_channelvideo_channelname'),
    ]

    operations = [
        migrations.AddField(
            model_name='channelvideo',
            name='slug',
            field=models.CharField(default=5, max_length=130),
            preserve_default=False,
        ),
    ]