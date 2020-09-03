from rest_framework import serializers

from .models import Dish, MenuCard


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['name', 'desc', 'price', 'preparation_time', 'vegetarian']


class MenuCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCard
        fields = ['name', 'desc', 'dishes']
