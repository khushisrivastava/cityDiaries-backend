from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField


class Place(models.Model):
    """Model definition for Places."""
    TYPE_CHOICE = (
        ("gym", "Gym"),
        ("restaurant", "Restaurant"),
        ("lodging", "Lodging")
    )
    type = models.CharField(choices=TYPE_CHOICE, default=None, max_length=10)
    icon = models.TextField(blank=True)
    name = models.CharField(max_length=225, blank=True)
    place_id = models.CharField(max_length=225, unique=True)
    address = models.TextField(blank=True)
    rating = models.DecimalField(blank=True, max_digits=2, decimal_places=1, null=True)

    class Meta:
        """Meta definition for Places."""

        verbose_name = 'place'
        verbose_name_plural = 'places'

    def __str__(self):
        return f'{self.id}'


class Review(models.Model):
    """Model definition for Review."""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='place_reviews')
    review = JSONField()

    class Meta:
        """Meta definition for Review."""

        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return f'{self.user.id}: {self.place.name}'


class Question(models.Model):
    TYPE_CHOICE = (
        ("gym", "Gym"),
        ("restaurant", "Restaurant"),
        ("lodging", "Lodging")
    )
    type = models.CharField(choices=TYPE_CHOICE, default=None, max_length=10)
    question = models.TextField(blank=True)

    class Meta:
        """Meta definition for Review."""

        verbose_name = 'question'
        verbose_name_plural = 'questions'

    def __str__(self):
        return f'{self.id}: {self.type}'


class Photos(models.Model):
    photo_reference = models.CharField(max_length=255, unique=True)
    photo = models.FileField(blank=True, null=True, upload_to="pranrate/photo")
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    def __str__(self):
        return self.photo_reference


class Cities(models.Model):
    country = models.CharField(max_length=2, blank=True)
    region = models.CharField(max_length=3, blank=True)
    url = models.CharField(max_length=225, blank=True)
    name = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=16, blank=True, null=True)
    longitude = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return f'{self.name}'