from django.db import models, transaction


class BoardingPoint(models.Model):
    name = models.CharField(max_length=255, help_text="Ex: Praça Central, Posto Shell")
    address_reference = models.CharField(
        max_length=255, blank=True, null=True, help_text="Ex: Em frente à farmácia"
    )
    route_order = models.PositiveIntegerField(
        default=0, help_text="Ordem em que o motorista passa no ponto (0, 1, 2...)"
    )

    class Meta:
        ordering = ["route_order"]

    def __str__(self):
        return f"{self.route_order}: {self.name}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = BoardingPoint.objects.get(pk=self.pk)
            old_order = old_instance.route_order
            new_order = self.route_order

            if old_order != new_order:
                if new_order < old_order:
                    BoardingPoint.objects.filter(
                        route_order__gte=new_order, route_order__lt=old_order
                    ).exclude(pk=self.pk).update(
                        route_order=models.F("route_order") + 1
                    )
                else:
                    BoardingPoint.objects.filter(
                        route_order__gt=old_order, route_order__lte=new_order
                    ).exclude(pk=self.pk).update(
                        route_order=models.F("route_order") - 1
                    )
        else:
            BoardingPoint.objects.filter(route_order__gte=self.route_order).update(
                route_order=models.F("route_order") + 1
            )

        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        deleted_order = self.route_order
        super().delete(*args, **kwargs)
        BoardingPoint.objects.filter(route_order__gt=deleted_order).update(
            route_order=models.F("route_order") - 1
        )
