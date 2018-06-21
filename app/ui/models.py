from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
import sys
import pytz
import logging
import json
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s-%(module)s-%(funcName)s-%(asctime)s :: %(message)s')

fh = logging.FileHandler('log_filename.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

sd_timezone = pytz.timezone('America/Los_Angeles')

class Base(models.Model):
    name          = models.CharField(default="Unknown...", max_length=200)
    created       = models.DateTimeField('Created date', auto_now_add=True, auto_now=False, null=True, blank=True)
    updated       = models.DateTimeField('Updated date', auto_now_add=False, auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta(object):
        abstract=True
        ordering=('name',)

class Address(Base):
    """
    Common address model.
    Can be used for Employee, SpareStore, Case (Breakdown location) etc.
    """
    gps_lattitude = models.FloatField(blank=True, null=True)
    gps_longitude = models.FloatField(blank=True, null=True)
    addr_line     = models.CharField(max_length=300)
    zipcode       = models.PositiveIntegerField(unique=False)


####################################################
# custom model manager
class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(user='admin')


class UserProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name     = models.CharField(default="FirstName", max_length=200)
    last_name      = models.CharField(default="LastName", max_length=200)
    nick_name      = models.CharField(default="NickName", max_length=200, blank=True, null=True)
    email          = models.EmailField()
    image          = models.ImageField(upload_to='profile_image', blank=True, null=True)
    admin          = UserProfileManager()

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile, sender=User)
####################################################

class Person(Base):
    """
    A human form has some basic requirements
    """
    first_name     = models.CharField(default="FirstName", max_length=200)
    last_name      = models.CharField(default="LastName", max_length=200)
    nick_name      = models.CharField(default="NickName", max_length=200, blank=True, null=True)
    GENDER_CHOICES  = [
                ('m', 'Male'),
                ('f', 'Female'),
                ('x', 'Other'),
            ]
    gender         = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    email_id       = models.EmailField(max_length=200)
    contact_no     = models.DecimalField(max_digits=10, decimal_places=0)
    dob            = models.DateField(blank=True, null=True)
    address        = models.OneToOneField('Address', on_delete=models.CASCADE)


class Place(Base):
    address        = models.OneToOneField('Address', on_delete=models.CASCADE)


class Task(Base):
    description = models.TextField()
    CHOICES=( ('ui', 'Urgent & Important'), ('u', 'Urgent'), ('i', 'Important'), ('tp', 'Not Urgent and Not Important'),)
    priority    = models.CharField(max_length=2, choices=CHOICES)
    along_with  = models.ManyToManyField('Person')
    who         = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    when        = models.DateTimeField()
    where       = models.ForeignKey('Place', on_delete=models.CASCADE)
    duration    = models.PositiveIntegerField()
    remind      = models.BooleanField(default=True)
