from django.db import models
from accounts.models import CustomUser


class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, blank=True)

    github_link = models.URLField(blank=True)
    live_demo = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title