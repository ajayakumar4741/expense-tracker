from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income','Income'),
        ('Expense','Expense')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_type = models.CharField(max_length=10,choices=TRANSACTION_TYPES)
    date = models.DateField()
    category = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title