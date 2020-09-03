from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dish, MenuCard
from .serializers import DishSerializer, MenuCardSerializer, MenuCardListSerializer
from .permissions import IsUser


@api_view(['POST'])
@permission_classes([IsUser])
def create_dish(request):
    serializer = DishSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsUser])
def modify_dish(request, pk):
    try:
        dish = Dish.objects.get(pk=pk)
    except Dish.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DishSerializer(dish, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsUser])
def create_menu_card(request):
    serializer = MenuCardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsUser])
def modify_menu_card(request, pk):
    try:
        menu = MenuCard.objects.get(pk=pk)
    except MenuCard.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MenuCardSerializer(menu, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuCardList(generics.ListAPIView):
    serializer_class = MenuCardListSerializer
    queryset = MenuCard.objects.filter(dishes__isnull=False)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'creation_date', 'last_modified']
    ordering_fields = ['name', 'dishes']


class MenuCardDetail(generics.RetrieveAPIView):
    queryset = MenuCard.objects.all()
    serializer_class = MenuCardSerializer
