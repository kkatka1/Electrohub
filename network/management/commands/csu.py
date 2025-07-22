from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.get(email="admin@sky.pro")
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                "admin", "admin@sky.pro", "123qwe456rty"
            )
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        except User.MultipleObjectsReturned:
            self.stdout.write(
                self.style.ERROR(
                    "Multiple superusers found, please check the database!"
                )
            )
