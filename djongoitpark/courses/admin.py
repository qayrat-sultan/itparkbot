from django.contrib import admin
from .models import Courses, Centers


class CoursesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Courses, CoursesAdmin)


class CentersAdmin(admin.ModelAdmin):
    pass


admin.site.register(Centers, CoursesAdmin)
