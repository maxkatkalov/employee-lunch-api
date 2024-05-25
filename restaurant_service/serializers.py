from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polling_service.models import Poll
from restaurant_service.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "address",
            "contact_number",
            "contact_email",
            "description",
            "website",
            "capacity",
            "cuisine_type",
        )


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "address",
            "cuisine_type",
            "capacity",
        )


class RestaurantDetailSerializer(RestaurantSerializer):
    owner_full_name = serializers.ReadOnlyField(source="owner.full_name")

    class Meta:
        model = Restaurant
        fields = RestaurantSerializer.Meta.fields + ("owner_full_name",)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class MenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ("poll",)

    def __init__(self, *args, **kwargs):
        super(MenuCreateSerializer, self).__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["restaurant"].queryset = Restaurant.objects.filter(
            owner=user
        ).select_related("owner")

    def create(self, validated_data):
        restaurant = validated_data.get("restaurant")
        poll = Poll.objects.filter(
            is_closed=False
        ).first()  # Adjust this logic as per your needs

        validated_data["poll"] = poll

        if Menu.objects.filter(restaurant=restaurant, poll=poll).exists():
            raise ValidationError(
                "A menu for this restaurant and poll already exists."
            )

        return super(MenuCreateSerializer, self).create(validated_data)
