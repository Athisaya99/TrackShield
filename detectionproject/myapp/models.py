from django.db import models
from django.contrib.auth.models import User



class Train(models.Model):
    trainname=models.CharField(max_length=200)
    trainnumber=models.CharField(max_length=200)
    startingstation=models.CharField(max_length=200)
    endingstation=models.CharField(max_length=200)

class Locopilot(models.Model):
    USER=models.OneToOneField(User,on_delete=models.CASCADE)
    TRAIN = models.ForeignKey(Train, on_delete=models.CASCADE , null=True,blank=True)
    name=models.CharField(max_length=200)
    stationname=models.CharField(max_length=200)
    place=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    Email=models.CharField(max_length=200)


class Complaint(models.Model):
    LOCOPILOT=models.ForeignKey(Locopilot,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=200)
    reply=models.CharField(max_length=200)
    date=models.CharField(max_length=200)

class Camera(models.Model):
    TRAIN = models.ForeignKey(Train, on_delete=models.CASCADE,null=True,blank=True)
    cameraname=models.CharField(max_length=200)


class Alert(models.Model):
    LOCOPILOT=models.ForeignKey(Locopilot,on_delete=models.CASCADE)
    CAMERA=models.ForeignKey(Camera,on_delete=models.CASCADE)
    alerttype=models.CharField(max_length=200)
    message=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    time=models.CharField(max_length=200)
    status=models.CharField(max_length=200,default="pending")

class Cameraalert(models.Model):
    CAMERA=models.ForeignKey(Camera,on_delete=models.CASCADE)
    LOCOPILOT = models.ForeignKey(Locopilot, on_delete=models.CASCADE,null=True,blank=True)
    Image=models.FileField(upload_to='alert/')
    description=models.CharField(max_length=200)
    date=models.CharField(max_length=200)

class Awareness(models.Model):
    title=models.CharField(max_length=200)
    message=models.CharField(max_length=200)
    priority=models.CharField(max_length=200)
    date=models.DateField()
    time=models.TimeField()
    status=models.CharField(max_length=200)



