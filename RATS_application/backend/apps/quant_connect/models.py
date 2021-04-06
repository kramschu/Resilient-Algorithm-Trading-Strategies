from django.db import models

# Create your models here.
class User(models.Model):
    """Model for the users table"""
    # userid
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Backtest(models.Model):
    """Model for the backtests table"""
    # backtestid
    backtestid = models.AutoField(primary_key = True)
    algname = models.CharField(max_length=30)
    cash = models.DecimalField(max_digits=11, decimal_places=2)
    startdate = models.CharField(max_length=10)
    enddate = models.CharField(max_length=10)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    filepath = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)