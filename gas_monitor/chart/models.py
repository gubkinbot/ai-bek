from django.db import models

class GasRecord(models.Model):
    datetime       = models.DateTimeField()
    gas_rate_fact  = models.FloatField()
    gas_rate_plan  = models.FloatField()

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return f'{self.datetime} — факт {self.gas_rate_fact}'

class Annotation(models.Model):
    # Врэмя, к которому привязан комментарий (на оси X)
    timestamp = models.DateTimeField()
    # Текст комментария
    text = models.CharField("Комментарий", max_length=255)
    # Когда создана запись
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M} — {self.text}"
