import datetime

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from polling_service.models import Poll
from restaurant_service.models import Menu, Restaurant
from restaurant_service.serializers import (
    RestaurantSerializer,
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    MenuSerializer,
    MenuCreateSerializer,
)
from .permissions import IsSuperuserOrOwner


class DefaultSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 1000


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().select_related("owner")
    serializer_class = RestaurantSerializer
    pagination_class = DefaultSetPagination
    permission_classes = (IsAuthenticated, IsSuperuserOrOwner)

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantListSerializer
        if self.action == "retrieve":
            return RestaurantDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_owner:
            return Restaurant.objects.filter(owner=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = (
        Menu.objects.all().select_related("restaurant").order_by("-date_added")
    )
    serializer_class = MenuSerializer
    pagination_class = DefaultSetPagination
    permission_classes = (IsAuthenticated, IsSuperuserOrOwner)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "retrieve"):
            return MenuCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_owner:
            return (
                Menu.objects.select_related("restaurant")
                .filter(restaurant__owner=self.request.user)
                .order_by("-date_added")
            )
        return self.queryset

    def perform_create(self, serializer):
        poll = Poll.objects.get(created_at=datetime.date.today())
        serializer.save(poll=poll)
