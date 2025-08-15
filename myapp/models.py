from django.db import models

# Create your models here.
class loginTbl(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    utype=models.CharField(max_length=100)

class ownerTbl(models.Model):
    LOGIN=models.ForeignKey(loginTbl,on_delete=models.CASCADE)
    image=models.FileField()
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    phno=models.BigIntegerField()
    email=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.DateField(max_length=100)

class driverTbl(models.Model):
    LOGIN=models.ForeignKey(loginTbl,on_delete=models.CASCADE)
    OWNER=models.ForeignKey(ownerTbl,on_delete=models.CASCADE)
    image=models.FileField()
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    phno=models.BigIntegerField()
    license=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.DateField(max_length=100)

class boatTbl(models.Model):
    OWNER=models.ForeignKey(ownerTbl,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.FileField()
    regno=models.BigIntegerField()
    fitness=models.FileField()
    no_of_passengers=models.BigIntegerField()
    type=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    discription=models.TextField(max_length=100)
    certificate=models.FileField()
    qryt=models.FileField()
    status=models.CharField(max_length=20)

class locationTbl(models.Model):
    DRIVER=models.ForeignKey(driverTbl,on_delete=models.CASCADE)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)

class routeTbl(models.Model):
    fromRoute=models.CharField(max_length=100)
    to=models.CharField(max_length=100)

class stopTbl(models.Model):
    ROUTE=models.ForeignKey(routeTbl,on_delete=models.Model)
    name=models.CharField(max_length=100)

class timescheudle(models.Model):
    ROUTE=models.ForeignKey(routeTbl,on_delete=models.Model)
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    tripname=models.CharField(max_length=100)
    start_time=models.TimeField()
    end_time=models.TimeField()





class timescheudle_details(models.Model):
    timeschedule=models.ForeignKey(timescheudle,on_delete=models.CASCADE)
    STOP=models.ForeignKey(stopTbl,on_delete=models.CASCADE)
    Time=models.TimeField()


class emergencyTbl(models.Model):
    DRIVER=models.ForeignKey(driverTbl,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    details=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class insuranceTbl(models.Model):
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    policy_no=models.CharField(max_length=100)
    provider=models.CharField(max_length=100)
    date=models.DateField()
    validity=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class userTbl(models.Model):
    LOGIN=models.ForeignKey(loginTbl,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.BigIntegerField()
    phno = models.BigIntegerField()
    email = models.CharField(max_length=100)

class feedbackTbl(models.Model):
    USER=models.ForeignKey(userTbl,on_delete=models.CASCADE)
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    rating=models.FloatField()
    date = models.DateField()

class complaintTbl(models.Model):
    USER=models.ForeignKey(userTbl,on_delete=models.CASCADE)
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    date = models.DateField()
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)

class bookingTbl(models.Model):
    USER=models.ForeignKey(userTbl,on_delete=models.CASCADE)
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    fromRoute=models.CharField(max_length=100)
    to= models.CharField(max_length=100)
    date=models.DateField()
    no_of_passengers=models.BigIntegerField()
    status=models.CharField(max_length=100)

class notificationTbl(models.Model):
    DRIVER=models.ForeignKey(driverTbl,on_delete=models.CASCADE)
    OWNER=models.ForeignKey(ownerTbl,on_delete=models.CASCADE)
    notification=models.TextField()
    date = models.DateField()

class camera_notificationTbl(models.Model):
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    image=models.FileField()
    type=models.CharField(max_length=100)
    date = models.DateField()
    time=models.TimeField()
    status=models.CharField(max_length=100)

class assign_table(models.Model):
    BOAT=models.ForeignKey(boatTbl,on_delete=models.CASCADE)
    DRIVER=models.ForeignKey(driverTbl,on_delete=models.CASCADE)
    status=models.CharField(max_length=100)




