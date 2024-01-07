from django.db import models
from .validators import validate_file_extension
from django.contrib.auth.models import User

class OperationUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
class ClientUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
class FileSystem(models.Model):
    file = models.FileField(upload_to="Uploads/",validators=[validate_file_extension])
    uploaded_by = models.ForeignKey(OperationUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    
class NewUserOtp(models.Model):
    email = models.CharField(max_length=30)
    otp = models.IntegerField(null=True,blank=True)
    