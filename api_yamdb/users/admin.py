from django.contrib import admin

from .models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'role'
    )
    list_display_links = ('username',)
    search_fields = ('username', 'last_name')


admin.site.register(User, UsersAdmin)
