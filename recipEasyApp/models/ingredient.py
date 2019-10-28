from django.db import models
from .location import Location


class Ingredient(models.Model):

    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("ingredient")
        verbose_name_plural = ("ingredients")