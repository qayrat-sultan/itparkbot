from django.contrib import admin

from .models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'registered')


admin.site.register(Users, UsersAdmin)
