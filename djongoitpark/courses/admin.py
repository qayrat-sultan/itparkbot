from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Courses, Centers


class CoursesAdmin(TranslationAdmin):
    pass


admin.site.register(Courses, CoursesAdmin)


class CentersAdmin(TranslationAdmin):
    pass


admin.site.register(Centers, CoursesAdmin)
