from django.contrib import admin

from .models import Title, Category, Review

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Review)