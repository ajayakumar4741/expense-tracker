from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='', blank=True, null=True)    
    phone = models.PositiveBigIntegerField(blank=True,null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    
   
    
    def __str__(self):
        return self.user.username
    
    





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
    
class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10,decimal_places=2)
    deadline = models.DateField()
    
    def __str__(self):
        return self.name
    
