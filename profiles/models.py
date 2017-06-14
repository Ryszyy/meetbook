from django.db import models
from django.contrib.auth.models import User, Group
from .utils import unique_slug_generator
from django.db.models.signals import pre_save


def pre_save_reciver_page_model(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = unique_slug_generator(instance)

class Location(models.Model):
    city = models.CharField(max_length=120)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.city


def upload_location(instance, filename):
    location = str(instance.user_auth.username)
    return f'{location}/{filename}'


class Intrest(models.Model):
    """docstring for Intrest"""
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    friends = models.ManyToManyField('self',
                                     blank=True)
    pending = models.ManyToManyField('self',
                                     blank=True,
                                     through="Invite",
                                     through_fields=('r_to', 'r_from'),
                                     symmetrical=False)
    bio = models.TextField(blank=True, null=True)
    time = models.ManyToManyField("profiles.FreeTime",
                                  blank=True)

    def __str__(self):
        return self.user_auth.username


pre_save.connect(pre_save_reciver_page_model, sender=UserProfile)


class GroupProfile(models.Model):
    """docstring for GroupProfile"""
    name = models.CharField(max_length=120, unique=True)
    owner = models.ForeignKey(UserProfile, related_name="owner")
    intrest = models.ManyToManyField(Intrest)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    members = models.ManyToManyField(UserProfile)
    slug = models.SlugField(blank=True)
    message = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


pre_save.connect(pre_save_reciver_page_model, sender=GroupProfile)


class FreeTime(models.Model):
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    group = models.ForeignKey(GroupProfile)
    user = models.ForeignKey(UserProfile)


    def __str__(self):
        readable_start = str(self.start_date)[5:]
        readable_start = readable_start[:-9]
        readable_end = str(self.end_date)[5:]
        readable_end = readable_end[:-9]
        return f"{readable_start} - {readable_end}"


class Invite(models.Model):
    r_from = models.ForeignKey(UserProfile, blank=True, related_name="r_from")
    r_to = models.ForeignKey(UserProfile, blank=True, related_name="r_to")
    when = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['r_from', 'r_to']

    def __str__(self):
        return (f'From {self.r_from} to {self.r_to}')


class Event(models.Model):
    name = models.CharField(max_length=120)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    intrest = models.ForeignKey(Intrest)
    members = models.ManyToManyField(UserProfile, blank=True)
    slug = models.SlugField(blank=True)
    creator = models.ForeignKey(UserProfile, related_name="creator", blank=True, null=True)
    group = models.ForeignKey(GroupProfile, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


pre_save.connect(pre_save_reciver_page_model, sender=Event)
