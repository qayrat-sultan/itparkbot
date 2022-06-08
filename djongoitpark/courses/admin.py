from django.contrib import admin
from .models import Courses, Centers
from django.utils.safestring import mark_safe


class CoursesAdmin(admin.ModelAdmin):
    exclude = ('slug', 'image')

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image_file.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


admin.site.register(Courses, CoursesAdmin)


class CentersAdmin(admin.ModelAdmin):
    exclude = ('slug', 'image')

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image_file.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


admin.site.register(Centers, CoursesAdmin)
