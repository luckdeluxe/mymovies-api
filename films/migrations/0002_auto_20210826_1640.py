# Generated by Django 3.2.6 on 2021-08-26 16:40

from django.db import migrations, models
import films.models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='image_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=films.models.Film.path_to_film, verbose_name='Thumbnail'),
        ),
        migrations.AddField(
            model_name='film',
            name='image_wallpaper',
            field=models.ImageField(blank=True, null=True, upload_to=films.models.Film.path_to_film, verbose_name='Wallpaper'),
        ),
    ]