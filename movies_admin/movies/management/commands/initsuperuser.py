import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get('SUPERUSER_USERNAME')
        email = os.environ.get('SUPERUSER_EMAIL')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            raise Exception('Not enough fields for creating superuser')

        try:
            User = get_user_model()

            if User.objects.filter(username=username, is_superuser=True).exists():
                self.stdout.write(
                    self.style.NOTICE(
                        'Superuser found. Skipping superuser creation')
                )
                return

            self.stdout.write(
                self.style.NOTICE('Superuser not found, creating one')
            )
            User.objects.create_superuser(
                username, email, password
            )
            self.stdout.write(
                self.style.SUCCESS('A superuser was created')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Creating superuser exception occured: {e}')
            )
