import uuid
from django.db import models
from django.utils.text import slugify

class Film(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150, verbose_name='Title')
    year = models.PositiveIntegerField(default=2000, verbose_name='Year')
    review_short = models.TextField(null=True, blank=True, verbose_name='Argument (short)')
    review_large = models.TextField(null=True, blank=True, verbose_name='History (large)')
    trailer_url = models.URLField(max_length=150, null=True, blank=True, verbose_name='Url youtube')
    genres = models.ManyToManyField('FilmGenre', related_name='film_genres', verbose_name='Genders')


    class Meta:
        verbose_name = "Movie"
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.year})'
    
    def path_to_film(self, instance, filename):
        return f'films/{instance.id}/{filename}'

    image_thumbnail = models.ImageField(upload_to=path_to_film, null=True, blank=True, verbose_name="Thumbnail")
    image_wallpaper = models.ImageField(upload_to=path_to_film, null=True, blank=True, verbose_name="Wallpaper")

class FilmGenre(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Name", unique=True)
    slug = models.SlugField(
        unique=True)

    class Meta:
        verbose_name = "Gender"
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(FilmGenre, self).save(*args, **kwargs)


