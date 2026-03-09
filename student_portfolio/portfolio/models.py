from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


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


# 👇 THIS MUST EXIST
class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    github_link = models.URLField(blank=True)
    live_demo = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title