"""meetbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from profiles.views import create_user, logout
from profiles.views.cbv.user_crud import UserDetailView, UsersList, user_delete, user_update, test
from profiles.views.cbv.friend_crud import friend_add, friend_delete
from profiles.views.cbv.event_crud import EventsList, PastEventsList, EventDetailView, event_join, event_create, event_delete, member_delete, event_update, EMemberUpdate
from profiles.views.cbv.group_crud import GroupsList, GroupDetailView, group_create, group_delete, GMemberUpdate, date_add, group_event_create, EventGroupDetailView, message_creator

urlpatterns = [
    url(r'^$', create_user.page, name='welcome'),
    url(r'^logout$', logout.page, name='logout'),

    # users
    url(r'^users_list$', UsersList.as_view(), name="users_list"),
    url(r'^user_detail/(?P<slug>[-\w]+)$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user_delete/(?P<slug>[-\w]+)$', user_delete, name="user_delete"),
    url(r'^user_update/(?P<slug>[-\w]+)$', user_update, name="user_update"),

    url(r'^testmap$', test, name="testmap"),

    # friend
    url(r'^friend_add/(?P<slug>[-\w]+)$', friend_add, name="friend_add"),
    url(r'^friend_delete/(?P<slug>[-\w]+)$', friend_delete, name="friend_delete"),

    # events
    
    url(r'^events_list$', EventsList.as_view(), name="events_list"),
    url(r'^event_create$', event_create, name="event_create"),
    url(r'^event_detail/(?P<slug>[-\w]+)$', EventDetailView.as_view(), name='event_detail'),
    url(r'^event_update/(?P<slug>[-\w]+)$', event_update, name="event_update"),
    url(r'^event_join/(?P<slug>[-\w]+)$', event_join, name="event_join"),
    url(r'^event_delete/(?P<slug>[-\w]+)$', event_delete, name="event_delete"),
    url(r'^past_events$', PastEventsList.as_view(), name="past_events"),
    url(r'^event_members/(?P<slug>[-\w]+)$', EMemberUpdate.as_view(), name="event_members"),
    url(r'^event_member_delete/(?P<slug>[-\w]+)$', member_delete, name="event_member_delete"),


    # groups
    url(r'^groups_list$', GroupsList.as_view(), name="groups_list"),
    url(r'^group_detail/(?P<slug>[-\w]+)$', GroupDetailView.as_view(), name="group_detail"),
    url(r'^group_create$', group_create, name="group_create"),
    # url(r'^group_update/(?P<slug>[-\w]+)$', group_update, name="group_update"),
    url(r'^group_delete/(?P<slug>[-\w]+)$', group_delete, name="group_delete"),
    url(r'^group_members/(?P<slug>[-\w]+)$', GMemberUpdate.as_view(), name="group_members"),
    url(r'^date_add/(?P<slug>[-\w]+)$', date_add, name="date_add"),
    url(r'^group_event_create/(?P<slug>[-\w]+)$', group_event_create, name="group_event_create"),
    url(r'^event_group/(?P<slug>[-\w]+)$', EventGroupDetailView.as_view(), name='event_group'),
    url(r'^message_creator/(?P<slug>[-\w]+)$', message_creator, name='message_creator'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
