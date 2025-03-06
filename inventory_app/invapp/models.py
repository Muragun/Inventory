from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class ItemType(models.Model):
    """Категория инвентаря (например, ноутбук, принтер, мебель)"""
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Название категории")
    )

    class Meta:
        verbose_name = _("Тип предмета")
        verbose_name_plural = _("Типы предметов")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    """Местоположение предметов (например, аудитория, склад)"""
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Название местоположения")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Описание")
    )

    class Meta:
        verbose_name = _("Местоположение")
        verbose_name_plural = _("Местоположения")
        ordering = ["name"]

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    """Основной объект инвентаризации"""
    name = models.CharField(
        max_length=255,
        verbose_name=_("Название предмета")
    )
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.PROTECT,
        related_name="items",
        verbose_name=_("Тип предмета")
    )
    serial_number = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Серийный номер")
    )
    inventory_number = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Инвентарный номер")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Описание")
    )
    purchase_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Дата покупки")
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Стоимость")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активен")
    )

    class Meta:
        verbose_name = _("Предмет инвентаря")
        verbose_name_plural = _("Предметы инвентаря")
        ordering = ["name"]
        unique_together = ["name", "serial_number"]

    def __str__(self):
        return f"{self.name} ({self.serial_number or 'Без номера'})"


class ItemLocationAssignment(models.Model):
    """Связь предметов с местоположениями"""
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name=_("Предмет")
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name=_("Местоположение")
    )
    assigned_at = models.DateTimeField(
        default=now,
        verbose_name=_("Дата размещения")
    )
    removed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Дата удаления")
    )

    class Meta:
        verbose_name = _("Распределение предмета")
        verbose_name_plural = _("Распределение предметов")
        ordering = ["-assigned_at"]
        constraints = [
            models.UniqueConstraint(fields=["item", "location"], name="unique_item_location")
        ]

    def __str__(self):
        return f"{self.item.name} → {self.location.name} ({self.assigned_at})"

    def remove_from_location(self):
        """Метод для снятия предмета с учета (фиксируем дату удаления)"""
        self.removed_at = now()
        self.save()


class ItemAssociation(models.Model):
    """Связь между инвентарными предметами (например, компьютер и монитор)"""
    parent_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='child_associations',
        verbose_name=_("Родительский предмет")
    )
    child_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='parent_associations',
        verbose_name=_("Дочерний предмет")
    )

    class Meta:
        verbose_name = _("Связь предметов")
        verbose_name_plural = _("Связи предметов")
        unique_together = ("parent_item", "child_item")
        ordering = ['parent_item', 'child_item']

    def __str__(self):
        return f"{self.parent_item.name} → {self.child_item.name}"

