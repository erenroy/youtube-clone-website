# Generated by Django 4.1.3 on 2023-11-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_channelvideo_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelvideo',
            name='category',
            field=models.CharField(choices=[('A', 'Action'), ('AN', 'Animes'), ('K', 'Film'), ('G', 'Gaming'), ('L', 'Learing'), ('F', 'Fashion'), ('S', 'Sports')], default='A', max_length=25),
        ),
    ]
