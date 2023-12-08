from django.db import models




class WireData(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    level = models.FloatField()
    status = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"WireData - {self.datetime}"
    
    def save(self, *args, **kwargs):
        # Check if level is 90
        if self.level == 90:
            # If the last 20 entries in the database have the same level, set status to 'low check IV bag pipe'
            last_20_entries = WireData.objects.order_by('-datetime').filter(level=90)[:20]
            if len(last_20_entries) == 20 and all(entry.level == 90 for entry in last_20_entries):
                self.status = 'low check IV bag pipe'
            else:
                self.status = 'normal'
        elif self.level == 50:
            self.status = 'low check IV bag pipe'

        super().save(*args, **kwargs)