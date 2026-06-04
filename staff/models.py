from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved_days = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    days = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.days = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)