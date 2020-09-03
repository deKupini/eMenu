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


class MenuCardListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'name': instance.name,
            'desc': instance.desc,
            'creation_date': instance.creation_date,
            'last_modified': instance.last_modified,
            'dishes': instance.dishes.count()
        }


class DishDetailSerializer(DishSerializer):
    class Meta:
        fields = ['creation_date', 'last_modified']


class MenuCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCard
        fields = ['name', 'desc', 'dishes', 'creation_date', 'last_modified']
        depth = 1
    # dishes = DishSerializer(many=True)