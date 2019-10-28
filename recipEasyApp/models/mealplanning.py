from django.db import models
from .customer import Customer
from .recipe import Recipe


class MealPlanning(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)