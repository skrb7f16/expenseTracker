from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Categories(models.Model):
    title=models.CharField(unique=True,max_length=255)
    at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class Expenses(models.Model):
    idOfExpense=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    amount=models.FloatField()
    category=models.ForeignKey(to='Categories',on_delete=models.CASCADE)
    at=models.DateTimeField(default=timezone.now())
    atDate=models.DateField(default=timezone.now())
    by=models.ForeignKey(to=User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title+" "+str(self.amount)
    