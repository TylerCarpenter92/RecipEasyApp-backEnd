from django.db import models
from .recipe import Recipe
from .ingredient import Ingredient

class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    extra_instructions = models.CharField(max_length=1000)

