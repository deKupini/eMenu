import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import datetime as dt
from .models import Dish, MenuCard


class CreateDishTest(APITestCase):
    """Test creating new dishes"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.valid_payload = {
            'name': 'Pizza 4 sery',
            'desc': 'Mozzarella, pleśniowy, cheddar, masdamer',
            'price': 24,
            'preparation_time': 20,
            'vegetarian': True
        }

    def test_create_dish_without_authorization(self):
        response = self.client.post(reverse('create_dish'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_dish_with_authorization(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.post(reverse('create_dish'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        dish = Dish.objects.get(id=1)
        self.assertEqual(dish.name, self.valid_payload['name'])
        self.assertEqual(dish.desc, self.valid_payload['desc'])
        self.assertEqual(dish.price, self.valid_payload['price'])
        self.assertEqual(dish.preparation_time, self.valid_payload['preparation_time'])
        self.assertEqual(dish.vegetarian, self.valid_payload['vegetarian'])
        self.assertEqual(dish.creation_date.__str__(), dt.today().strftime('%Y-%m-%d'))


class ModifyDishTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.dish = Dish.objects.create(name='Schabowy', desc='Kotlet schabowy z ziemniakami', price=15,
                                        preparation_time=15, creation_date='1900-01-01', last_modified='1900-01-02',
                                        vegetarian=False)
        self.before_modify_creation_date = self.dish.creation_date
        self.valid_payload = {
            'name': 'Sojowy kotlet schabowy',
            'desc': 'Kotlet z ziemniakami i surówką',
            'price': 18,
            'preparation_time': 20,
            'vegetarian': True
        }

    def test_modify_dish_without_authorization(self):
        response = self.client.put(reverse('modify_dish', kwargs={'pk': self.dish.pk}), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_dish(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.put(reverse('modify_dish', kwargs={'pk': self.dish.pk}), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, self.valid_payload['name'])
        self.assertEqual(self.dish.desc, self.valid_payload['desc'])
        self.assertEqual(self.dish.price, self.valid_payload['price'])
        self.assertEqual(self.dish.preparation_time, self.valid_payload['preparation_time'])
        self.assertEqual(self.dish.vegetarian, self.valid_payload['vegetarian'])
        self.assertEqual(self.dish.creation_date, self.before_modify_creation_date)
        self.assertEqual(self.dish.last_modified.__str__(), dt.today().strftime('%Y-%m-%d'))


class CreateMenuCardTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.dish_1 = Dish.objects.create(name='Schabowy', desc='Kotlet schabowy z ziemniakami', price=15,
                                          preparation_time=15, creation_date='1900-01-01', last_modified='1900-01-02',
                                          vegetarian=False)
        self.dish_2 = Dish.objects.create(name='Sałatka', desc='Sałata z majonezem', price=7, preparation_time=3,
                                          creation_date='1900-01-01', last_modified='1900-01-02', vegetarian=True)
        self.valid_payload = {
            'name': 'Menu tradycyjne',
            'desc': 'Menu dla każdego lokalu',
            'dishes': [self.dish_1.id, self.dish_2.id]
        }
        self.invalid_payload = {
            'name': 'Menu tradycyjne',
            'desc': 'Ukradzione menu',
            'dishes': [self.dish_1.id, self.dish_2.id]
        }

    def test_create_menu_card_without_authorization(self):
        response = self.client.post(reverse('create_menu_card'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_card(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.post(reverse('create_menu_card'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        menu = MenuCard.objects.get(id=1)
        self.assertEqual(menu.name, self.valid_payload['name'])
        self.assertEqual(menu.desc, self.valid_payload['desc'])
        self.assertEqual(menu.dishes.count(), len(self.valid_payload['dishes']))

    def test_create_menu_card_with_invalid_payload(self):
        self.client.login(username=self.user.username, password='12345')
        self.client.post(reverse('create_menu_card'), self.valid_payload)
        response = self.client.post(reverse('create_menu_card'), self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModifyMenuCardTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.dish_1 = Dish.objects.create(name='Schabowy', desc='Kotlet schabowy z ziemniakami', price=15,
                                          preparation_time=15, creation_date='1900-01-01', last_modified='1900-01-02',
                                          vegetarian=False)
        self.dish_2 = Dish.objects.create(name='Sałatka', desc='Sałata z majonezem', price=7, preparation_time=3,
                                          creation_date='1900-01-01', last_modified='1900-01-02', vegetarian=True)
        self.menu_1 = MenuCard.objects.create(name='Menu', desc='menu', creation_date='1900-01-01',
                                              last_modified='1900-01-01')
        self.menu_2 = MenuCard.objects.create(name='Menu2', desc='menu2', creation_date='1900-01-01',
                                              last_modified='1900-01-01')
        self.menu_1.dishes.add(self.dish_1.pk)
        self.before_modify_creation_date = self.menu_1.creation_date
        self.valid_payload = {
            'name': 'Menu tradycyjne',
            'desc': 'Menu dla każdego lokalu',
            'dishes': [self.dish_1.id, self.dish_2.id]
        }
        self.invalid_payload = {
            'name': 'Menu',
            'desc': 'Ukradzione menu',
            'dishes': [self.dish_1.id, self.dish_2.id]
        }

    def test_modify_menu_card_without_authorization(self):
        response = self.client.put(reverse('modify_menu_card', kwargs={'pk': self.menu_1.pk}), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_menu_card(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.put(reverse('modify_menu_card', kwargs={'pk': self.menu_1.pk}), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.menu_1.refresh_from_db()
        self.assertEqual(self.menu_1.name, self.valid_payload['name'])
        self.assertEqual(self.menu_1.desc, self.valid_payload['desc'])
        self.assertEqual(self.menu_1.dishes.count(), len(self.valid_payload['dishes']))
        self.assertEqual(self.menu_1.creation_date, self.before_modify_creation_date)
        self.assertEqual(self.menu_1.last_modified.__str__(), dt.today().strftime('%Y-%m-%d'))

    def test_modify_menu_card_with_invalid_payload(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.put(reverse('modify_menu_card', kwargs={'pk': self.menu_2.pk}), self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
