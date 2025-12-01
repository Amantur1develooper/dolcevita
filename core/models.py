# menu/models.py
from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("Название"), max_length=120)
    name_ky = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Аталышы (KY)")
    name_en = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Name (EN)")
    slug = models.SlugField( blank=True, null=True,)

    # новый порядок
    order = models.PositiveIntegerField(_("Порядок"), null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["order", "name"]  # ← теперь по номеру, потом по названию

    def save(self, *args, **kwargs):
        if not self.order or self.order == 0:
            max_order = Category.objects.aggregate(Max("order"))["order__max"] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)

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

    # новый порядок внутри категории
    order = models.PositiveIntegerField(_("Порядок в категории"),null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        # важно: сначала по категории, затем по нашему номеру, затем по имени
        ordering = ["category", "order", "name"]
        # уникальность номера в пределах категории
        constraints = [
            models.UniqueConstraint(fields=["category", "order"], name="uq_product_category_order")
        ]

    def save(self, *args, **kwargs):
        if (not self.order or self.order == 0) and self.category_id:
            max_order = (
                Product.objects.filter(category=self.category)
                .aggregate(Max("order"))["order__max"] or 0
            )
            self.order = max_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
