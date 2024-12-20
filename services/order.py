from datetime import datetime

from django.db.models import QuerySet

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username: str, date: datetime = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date if date else datetime.now())
        tickets_instances = []
        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket["movie_session"])
            tickets_instances.append(
                Ticket(order=order, movie_session=movie_session, row=ticket["row"], seat=ticket["seat"])
            )
        Ticket.objects.bulk_create(tickets_instances)
        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
