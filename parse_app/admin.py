from django.contrib import admin

# Register your models here.
from parse_app.models import Share, Trader


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'share',)
