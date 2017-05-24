from django.db import models
from django.contrib.auth.models import User, Group
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
# from django.core.exceptions import ValidationError
# Create your models here.


class Location(models.Model):
    city = models.CharField(max_length=120, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.city


def upload_location(instance, filename):
    location = str(instance.user_auth.username)
    return f'{location}/{filename}'


class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True)
    bio = models.TextField(blank=True, null=True)

    # def clean(self):
    #     if self.user_auth in self.friends:
    #         raise ValidationError("Can't do that")

    def __str__(self):
        return self.user_auth.username


def pre_save_reciver_page_model(sender, instance, *args, **kwargs):
    if instance.slug == 'page-slug' or instance.slug == '':
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_reciver_page_model, sender=UserProfile)


# class Friends(models.Model):
#     """docstring for ClassName"""
#     user = models.ForeignKey(UserProfile, related_name="User", on_delete=models.CASCADE)
#     friends = models.ManyToManyField(UserProfile, related_name="List")

#     class Meta:
#         verbose_name_plural = "friends"

#     def __str__(self):
#         return str(self.user) + "'s friends"


class Intrest(models.Model):
    """docstring for Intrest"""
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class GroupProfile(models.Model):
    """docstring for GroupProfile"""
    group = models.OneToOneField(Group, unique=True)
    owner = models.ForeignKey(UserProfile, related_name="owner")
    intrest = models.ManyToManyField(Intrest)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    members = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.group.name


class Event(models.Model):
    name = models.CharField(max_length=120)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    intrest = models.ForeignKey(Intrest)

    def __str__(self):
        return self.name
