from django.db import models
from .customer import Customer
from .ingredient import Ingredient


class Recipe(models.Model):


    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instructions = models.TextField(null=True, blank=True)
    time_to_cook = models.CharField(max_length=50, null=True, blank=True)
    link_to_page = models.CharField( max_length=1000, null=True, blank=True)
    ingredient_list = models.ManyToManyField("Ingredient", through="RecipeIngredient")


    class Meta:
        verbose_name = ("recipe")
        verbose_name_plural = ("recipes")