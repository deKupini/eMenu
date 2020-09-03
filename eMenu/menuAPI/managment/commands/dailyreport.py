from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Dish
from django.core.mail import send_mail
from datetime import date as dt, timedelta as td


class Command(BaseCommand):
    commands = ['sendreport', ]
    args = '[command]'
    help = 'Send report'

    def handle(self, *args, **options):
        yesterday = dt.today() - td(1)
        new_dishes = Dish.objects.filter(creation_date=yesterday).values_list('name', flat=True)
        modified_dishes = Dish.object.filter(last_modified=yesterday, creation_date__lt=yesterday).values_list('name',
                                                                                                               flat=True
                                                                                                               )
        new_dishes_text = '\n'.join(new_dishes)
        modified_dishes_text = '\n'.join(modified_dishes)

        report_text = """
        New dishes added yesterday:\n
        {}\n\n
        Dishes modified yesterday:\n
        {}
        """.format(new_dishes_text, modified_dishes_text)

        user_emails = User.objects.all().values_list('email', flat=True)

        send_mail(
            'Daily report of dishes',
            report_text,
            'reporter@emenu.com',
            user_emails,
            fail_silently=False,
        )
