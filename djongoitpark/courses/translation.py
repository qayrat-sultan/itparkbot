from modeltranslation.translator import (
    translator,
    register,
    TranslationOptions
)
from courses.models import Courses, Centers


class CoursesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    empty_values = ''


translator.register(Courses, CoursesTranslationOptions)


class CentersTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    empty_values = ''


translator.register(Centers, CoursesTranslationOptions)
