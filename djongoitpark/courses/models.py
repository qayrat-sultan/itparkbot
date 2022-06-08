from django.db import models

from .utils import send_photo


class Courses(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    price = models.CharField(verbose_name="Price", max_length=20)
    duration = models.CharField(verbose_name="Duration", max_length=20)
    image = models.CharField(max_length=100)
    image_file = models.ImageField()

    __original_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image_file

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.image_file != self.__original_image:
            self.image = send_photo(self.image_file)
        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_image = self.image_file


class Centers(models.Model):
    title = models.CharField(max_length=30)
    phone = models.CharField(verbose_name="Phone number", max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.CharField(max_length=100)
    image_file = models.ImageField()

    __original_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image_file

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.image_file != self.__original_image:
            self.image = send_photo(self.image_file)
        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_image = self.image_file
