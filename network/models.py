from django.db import models
from rest_framework.exceptions import ValidationError

from .validators import check_supplier_chain


class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house_number}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    model = models.CharField(max_length=255, verbose_name="Модель продукта")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class NetworkPoint(models.Model):
    """Модель создания сети"""

    FACTORY = "factory"
    RETAIL = "retail"
    ENTREPRENEUR = "entrepreneur"

    LEVEL_CHOICES = (
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (ENTREPRENEUR, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    level = models.CharField(
        max_length=30, choices=LEVEL_CHOICES, verbose_name="Уровень звена"
    )
    contacts = models.ForeignKey(
        "Contact",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Контакты",
    )
    products = models.ManyToManyField("Product", verbose_name="Продукты")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="before_supplier",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Задолженность"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def clean(self):
        if self.level == NetworkPoint.FACTORY:
            if self.supplier is not None:
                raise ValidationError("Завод не может иметь поставщика.")

        elif self.level != NetworkPoint.FACTORY and self.supplier is None:
            raise ValidationError(
                f"{self.get_level_display()} должен иметь поставщика."
            )

        elif self.supplier and not check_supplier_chain(self):
            raise ValidationError(
                "Цепочка поставщиков не может быть более трех уровней."
            )

    class Meta:
        verbose_name = "Элемент сети"
        verbose_name_plural = "Элементы сети"

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
