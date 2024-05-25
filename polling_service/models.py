from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model


class Poll(models.Model):
    created_at = models.DateField(auto_now_add=True, unique=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Poll created at {self.created_at}"


class Vote(models.Model):
    created_at = models.DateField(auto_now_add=True)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="votes"
    )
    menu = models.ForeignKey(
        "restaurant_service.Menu",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    employee = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="votes"
    )

    class Meta:
        unique_together = ("created_at", "employee")

    def __str__(self) -> str:
        return (
            f"Vote created at {self.created_at} "
            f"for {self.menu_id} by {self.employee}"
        )
