from django.contrib import admin

from .models import CustomUser, Follow

admin.site.empty_value_display = '-пусто-'


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser')
    list_display_links = ('id', 'username')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
