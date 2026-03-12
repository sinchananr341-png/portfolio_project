from django.contrib import admin
from .models import PortfolioView, ResumeDownload

@admin.register(PortfolioView)
class PortfolioViewAdmin(admin.ModelAdmin):
    list_display = ('profile', 'ip_address', 'timestamp')
    list_filter = ('profile', 'timestamp')
    search_fields = ('profile__user__username', 'ip_address')

@admin.register(ResumeDownload)
class ResumeDownloadAdmin(admin.ModelAdmin):
    list_display = ('profile', 'ip_address', 'timestamp')
    list_filter = ('profile', 'timestamp')
    search_fields = ('profile__user__username', 'ip_address')
