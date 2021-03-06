from django.contrib import admin
from .models import Courses, Centers, Pages, ExternalLinks
from django.utils.safestring import mark_safe
from django.conf import settings


class CoursesAdmin(admin.ModelAdmin):  # noqa
    exclude = ('slug', 'image')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image_file.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


admin.site.register(Courses, CoursesAdmin)


class CentersAdmin(admin.ModelAdmin):  # noqa
    exclude = ('image', 'slug')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image_file.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


admin.site.register(Centers, CentersAdmin)  # noqa


class PagesAdmin(admin.ModelAdmin):  # noqa
    exclude = ('image',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image_file.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


admin.site.register(Pages, PagesAdmin)  # noqa


class ExternalLinksAdmin(admin.ModelAdmin):
    list_display = ('title', 'telegram_url')

    @admin.display(empty_value='Nothing')
    def telegram_url(self, obj):
        return 'https://t.me/' + settings.BOT_USERNAME + '/?start=' + str(obj.url)


admin.site.register(ExternalLinks, ExternalLinksAdmin)
