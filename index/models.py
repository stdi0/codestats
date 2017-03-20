from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Counter(models.Model):
    pos = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user_id = models.CharField(max_length=30)
    counter_for_all_time = models.IntegerField(default=0)
    counter_for_day = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

