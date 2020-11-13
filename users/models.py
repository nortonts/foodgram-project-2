from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def get_full_name(self):
        full_name = super().get_full_name()
        if not full_name:
            full_name = self.username
        return full_name.strip()
