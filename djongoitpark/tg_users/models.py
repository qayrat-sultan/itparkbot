from django.db import models


class Users(models.Model):
    id = models.IntegerField(unique=True, verbose_name='Telegram ID', editable=False, primary_key=True)
    fio = models.CharField(max_length=50, verbose_name='F.I.O.', blank=True, null=True)
    sex = models.CharField(max_length=15, verbose_name="Jinsi", blank=True, null=True)
    age = models.IntegerField(verbose_name="Yoshi", blank=True, null=True)
    phone = models.CharField(verbose_name="Telefoni raqam", max_length=20, blank=True, null=True)
    center = models.CharField(verbose_name="Markaz", max_length=20, blank=True, null=True)
    course = models.CharField(verbose_name="Kurs", max_length=20, blank=True, null=True)
    registered = models.BooleanField(default=False, verbose_name="Registratsiya qilgan")

    # def __str__(self):
    #     return self._id

    class Meta:
        db_table = 'users'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
