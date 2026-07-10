from django.contrib import admin
from .models import Hobby, HobbyLog


class HobbyLogInline(admin.TabularInline):
    model = HobbyLog
    extra = 0


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'status', 'priority', 'created_at')
    list_filter = ('category', 'status', 'priority')
    search_fields = ('name', 'user__username')
    inlines = [HobbyLogInline]


@admin.register(HobbyLog)
class HobbyLogAdmin(admin.ModelAdmin):
    list_display = ('hobby', 'date', 'duration_minutes', 'created_at')
    list_filter = ('date',)
