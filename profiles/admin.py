from django.contrib import admin
from profiles.models import UserProfile, Location, Intrest, GroupProfile, Event
# Register your models here.


# class ContactsListAdmin(admin.ModelAdmin):
#     """docstring for ContactsListAdmin"""
#     list_display = ('user',)

#     def __str__(self):
#         return str(self.username) + "'s friends"


admin.site.register(UserProfile)
admin.site.register(Location)
admin.site.register(Intrest)
admin.site.register(GroupProfile)
admin.site.register(Event)
