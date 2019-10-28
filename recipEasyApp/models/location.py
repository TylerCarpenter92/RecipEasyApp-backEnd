from django.db import models


class Location(models.Model):

    location = models.CharField(max_length=25)


    class Meta:
        verbose_name = ("location")
        verbose_name_plural = ("locations")