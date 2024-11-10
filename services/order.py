from django.contrib.auth import get_user_model
from django.db.models import QuerySet

import init_django_orm  # noqa: F401

from datetime import datetime
from django.db import transaction

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None):
    if not get_user_model().objects.filter(username=username).exists():
        user = get_user_model().objects.create_user(username=username)
    else:
        user = get_user_model().objects.get(username=username)

    order = Order(user=user)
    order.save()

    if date:
        datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.id).update(created_at=datetime_obj)

    for ticket in tickets:
        row = ticket.get("row")
        seat = ticket.get("seat")
        movie_session = MovieSession.objects.get(pk=ticket.get("movie_session"))

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()


if __name__ == "__main__":
    # tickets = [
    #     {
    #         "row": 6,
    #         "seat": 12,
    #         "movie_session": 1
    #     },
    #     {
    #         "row": 6,
    #         "seat": 13,
    #         "movie_session": 1
    #     }
    # ]
    # create_order(tickets=tickets, username="Username_1", date="2022-4-20 11:27")

    # tickets = [
    #     {
    #         "row": 5,
    #         "seat": 7,
    #         "movie_session": 1
    #     },
    #     {
    #         "row": 6,
    #         "seat": 9,
    #         "movie_session": 1
    #     }
    # ]
    # create_order(tickets=tickets, username="Username_1", date="2022-4-20 11:27")
    # create_order(tickets=tickets, username="Username_1", date="2022-9-20 11:27")
    # create_order(tickets=tickets, username="Username_2")

    # print(get_orders(username="Username_1"))
    # print(get_orders(username="admin.user"))
    # print(get_orders())
    # create_order(tickets=tickets, username="user_1", date="2020-11-10 14:40")
    # print(list(Order.objects.all().values_list("user__username")) == [("user_1",)])
    # print(Order.objects.all().values_list("user__username"))
    pass
