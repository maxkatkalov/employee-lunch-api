import os
import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from polling_service.models import Poll


class Restaurant(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    date_added = models.DateTimeField(auto_now_add=True)
    address = models.CharField(
        max_length=255,
        unique=True,
    )
    contact_number = models.CharField(max_length=40)
    contact_email = models.EmailField()
    description = models.TextField()
    website = models.URLField(null=True, blank=True)
    capacity = models.PositiveIntegerField()
    cuisine_type = models.CharField(max_length=100)

    owner = models.ForeignKey(
        get_user_model(), related_name="restaurants", on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=["name", "cuisine_type"]),
        ]

    def __str__(self) -> str:
        return (
            f"The {self.name} restaurant located at {self.address} "
            f"has a capacity of {self.capacity} people "
            f"and serves {self.cuisine_type} cuisine. "
            f"Contacts: {self.contact_number}|"
            f"{self.contact_email}|{self.website}"
        )


def menu_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    current_month = datetime.now().strftime("%Y/%m")
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/menus/", current_month, filename)


class Menu(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    menu_file = models.FileField(upload_to=menu_file_path)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="menus"
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "restaurant",
                ]
            ),
        ]

    def __str__(self) -> str:
        return (
            f"'{self.name}' menu for {self.restaurant}"
            f", for the day: {self.date_added}"
        )
