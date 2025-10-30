from django.db import models
from django.contrib.auth.models import AbstractUser
from app.rolechoices import RoleChoice
from app.manager import CustomUserManager
from app.timestamp import TimeStamp
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    image=models.ImageField(upload_to="Images/",null=True,blank=True)
    role=models.CharField(choices=RoleChoice.choices)
    username=models.CharField(blank=True, null=True)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]  

    objects = CustomUserManager()

class IPRequestLog(TimeStamp):
    ip_address = models.GenericIPAddressField()
    count = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now)
    last_request = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ip_address} - {self.count} requests"