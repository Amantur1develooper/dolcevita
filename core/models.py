# menu/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("Название"), max_length=120)
    name_ky = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Аталышы (KY)")
    name_en = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Name (EN)")

    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(_("Название"), max_length=180)
    name_ky = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Аталышы (KY)")
    name_en = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Name (EN)")

    slug = models.SlugField(unique=True)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu/", blank=True, null=True)
    # short_desc = models.CharField(_("Кратко"), max_length=220, blank=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
