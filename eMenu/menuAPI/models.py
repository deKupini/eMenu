from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=120)
    price = models.IntegerField()
    preparation_time = models.IntegerField()
    creation_date = models.DateField()
    last_modified = models.DateField()
    vegetarian = models.BooleanField()


class MenuCard(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)
    creation_date = models.DateField()
    last_modified = models.DateField()
    dishes = models.ManyToManyField(Dish)
