from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model
class CustomUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    portfolio_visibility = models.CharField(
        max_length=10,
        choices=[
            ('public', 'Public'),
            ('private', 'Private')
        ],
        default='public'
    )

    def __str__(self):
        return f"{self.user.username} Profile"