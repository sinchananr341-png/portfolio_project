from django.db import models
from portfolio.models import Profile

class PortfolioView(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"View on {self.profile.user.username} at {self.timestamp}"

class ResumeDownload(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='resume_downloads')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Resume downloaded for {self.profile.user.username} at {self.timestamp}"
