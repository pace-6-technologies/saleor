from django.db import models

class Region(models.Model):
    zipcode = models.CharField(max_length=10)
    province = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    language_code = models.CharField(max_length=5)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('province', 'city', 'district')
