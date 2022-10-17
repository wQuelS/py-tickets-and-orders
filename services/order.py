from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model
from django.db import transaction


def create_order(
        tickets: list[dict], username: str, date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        [
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all().order_by("-user")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
