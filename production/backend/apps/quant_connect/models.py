from django.db import models
from backend.apps.authentication.models import User
from django.conf import settings


class Backtest(models.Model):
    """Model for the backtests table"""
    # backtestid
    backtestid = models.AutoField(primary_key = True)
    algname = models.CharField(max_length=100)
    cash = models.DecimalField(max_digits=20, decimal_places=2)
    startdate = models.CharField(max_length=10)
    enddate = models.CharField(max_length=10)
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orig_filepath = models.CharField(max_length=1000)
    new_filepath = models.CharField(max_length=1000, default=None)
    time = models.DateTimeField(auto_now_add=True)
