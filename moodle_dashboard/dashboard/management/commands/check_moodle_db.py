from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Check the connection to the Moodle database'

    def handle(self, *args, **kwargs):
        db_conn = connections['moodle']
        try:
            c = db_conn.cursor()
        except OperationalError:
            self.stdout.write(self.style.ERROR('Unable to connect to the Moodle database'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully connected to the Moodle database'))
