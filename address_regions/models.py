from django.db import models

class Region(models.Model):
    postal_code = models.CharField(max_length=10)
    country_area = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    city_area = models.CharField(max_length=200)
    language_code = models.CharField(max_length=5)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('country_area', 'city', 'city_area')
