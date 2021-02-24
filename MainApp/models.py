from django.db import models

class User(models.Model):
    name = models.CharField(max_length=40)
    dob = models.DateField()
    email = models.CharField(max_length=40)
    mobile = models.CharField(max_length=15)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    bldgrp = models.CharField(max_length=20)
    profile = models.FileField()
    address = models.CharField(max_length=200,default='')

    def __str__(self):
        return self.username

class Request(models.Model):
    sender = models.CharField(max_length=40)
    reciever = models.CharField(max_length=40)
    bldgrp = models.CharField(max_length=20,default='')
    quantity = models.IntegerField()
    status = models.CharField(max_length=40)

    def __str__(self):
        return self.sender

class Bank(models.Model):
    bldgrp = models.CharField(max_length=20)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.bldgrp
