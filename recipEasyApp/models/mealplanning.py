from django.db import models
from .customer import Customer
from .recipe import Recipe
from datetime import datetime, date


class MealPlanning(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    week_number = models.SmallIntegerField(default=000)
    # day_of_week = models.SmallIntegerField(default=0)
    # year = models.SmallIntegerField(default=0000)

    @property
    def weekday(self):
        return self.date.strftime('%A')

    def weekday_number(self):
        return int(self.date.strftime('%w'))

    # def week_number(self):
    #     return self.date.strftime('%U')
