from django.db import models
from django.template.defaultfilters import slugify

from .utils import send_photo


class Courses(models.Model):
    title_uz = models.CharField(max_length=50, verbose_name='Тақырып атауы')
    title_ru = models.CharField(max_length=50, verbose_name='Название курса')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')
    description_uz = models.TextField(verbose_name='Тақырып колонкасы', blank=True, default="Tavsif")
    description_ru = models.TextField(verbose_name='Описание курса', blank=True, default="Описание")
    price = models.CharField(verbose_name="Narxi", max_length=20, default=0, blank=True)
    duration = models.CharField(verbose_name="Davomiyligi", max_length=20, default="None", blank=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    image_file = models.ImageField(upload_to='courses/', verbose_name='Курс тақырыпының суреті')

    __original_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image_file

    def __str__(self):
        return self.title_uz

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.image_file != self.__original_image:  # noqa
            self.image = send_photo(self.image_file)
        if not self.slug:
            self.slug = slugify(self.title_uz[:10])
        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_image = self.image_file

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'


class Centers(models.Model):
    title_uz = models.CharField(max_length=30, verbose_name='Центр атауы')
    title_ru = models.CharField(max_length=30, verbose_name='Название центра')
    description_uz = models.TextField(verbose_name='Тақырып колонкасы', blank=True, default="Tavsif")
    description_ru = models.TextField(verbose_name='Описание центра', blank=True, default="Описание")
    phone = models.CharField(verbose_name="Telefon raqam", max_length=20, default="None", blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    image_file = models.ImageField(upload_to='centers/', verbose_name='Центр тақырыпының суреті')

    __original_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image_file

    def __str__(self):
        return self.title_uz

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.image_file != self.__original_image:  # noqa
            self.image = send_photo(self.image_file)
        if not self.slug:
            self.slug = slugify(self.title_uz[:10])
        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_image = self.image_file

    class Meta:
        verbose_name = 'Markaz'
        verbose_name_plural = 'Markazlar'


class Pages(models.Model):
    title_uz = models.CharField(max_length=30, verbose_name='Бет атауы')
    title_ru = models.CharField(max_length=30, verbose_name='Название страницы')
    description_uz = models.TextField(verbose_name='Тақырып колонкасы', blank=True, default="Tavsif")
    description_ru = models.TextField(verbose_name='Описание страницы', blank=True, default="Описание")
    slug = models.SlugField(max_length=30, unique=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    image_file = models.ImageField(upload_to='pages/', verbose_name='Страница тақырыпының суреті')

    __original_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image_file

    def __str__(self):
        return self.title_uz

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.image_file != self.__original_image:  # noqa
            self.image = send_photo(self.image_file)
        if not self.slug:
            self.slug = slugify(self.title_uz[:10])
        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_image = self.image_file

    class Meta:
        verbose_name = 'Sahifa'
        verbose_name_plural = 'Sahifalar'
