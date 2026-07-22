from django.contrib import admin
from .models import Wish, GiftTransaction


@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'urgency', 'is_available', 'created_at']
    list_filter = ['is_available', 'urgency', 'created_at']
    search_fields = ['title', 'name']
    ordering = ['-created_at']


@admin.register(GiftTransaction)
class GiftTransactionAdmin(admin.ModelAdmin):
    list_display = ['wish', 'giver_name', 'gifted_at', 'is_reversed']
    list_filter = ['is_reversed', 'gifted_at']
    search_fields = ['wish__title', 'giver_name']
    ordering = ['-gifted_at']