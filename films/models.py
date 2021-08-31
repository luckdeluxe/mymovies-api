import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MaxValueValidator 
from django.db.models import Sum 
from django.db.models.signals import post_save 

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


class FilmUser(models.Model):

    STATUS_CHOICES = (
        (0, "Stateless"),
        (1, "View"),
        (2, "I want to see"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    # It could be done in three separate models to make it more efficient
    # But at the development level, you would have to do the same three times

    state = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=0)  #When created without state it is deleted
    favorite = models.BooleanField(
        default=False)
    note = models.PositiveSmallIntegerField(
        null=True, validators=[MaxValueValidator(10)])
    review = models.TextField(null=True)
    favorites = models.IntegerField(default=0, verbose_name="Favorites")
    average_note = models.FloatField(default=0.0, verbose_name="Average grade", 
        validators=[MaxValueValidator(10.0)])

    class Meta:
        unique_together = ['film', 'user']
        ordering = ['film__title']

def update_film_stats(sender, instance, **kwargs):
    # We update favorites by counting favorites from that movie
    count_favorites = FilmUser.objects.filter(
        film=instance.film, favorite=True).count()
    instance.film.favorites = count_favorites
    # We update the note by retrieving the number of notes and making the average
    notes = FilmUser.objects.filter(
        film=instance.film).exclude(note__isnull=True)
    count_notes = notes.count()
    sum_notes = notes.aggregate(Sum('note')).get('note__sum')
    # We try to make the mean to two decimal places using a try
    # It will fail if sum_notes is None as count_notes is 0
    # This happens the first few times because there are no notes set yet
    try:
        instance.film.average_note = round(sum_notes/count_notes, 2)
    except:
        pass
    # We save the movie
    instance.film.save()

# In the delete post the copy of the instance that no longer exists is passed
post_save.connect(update_film_stats, sender=FilmUser)


