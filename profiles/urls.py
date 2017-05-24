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

urlpatterns = [
    url(r'^$', create_user.page, name='welcome'),
    url(r'^logout$', logout.page, name='logout'),
    url(r'^users_list$', UsersList.as_view(), name="users_list"),
    url(r'^user_detail/(?P<slug>[-\w]+)$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user_delete/(?P<slug>[-\w]+)$', user_delete, name="user_delete"),
    # url(r'^user_delete/(?P<slug>[-\w]+)$', UserDelete.as_view(), name='user_delete'),
    url(r'^user_update/(?P<slug>[-\w]+)$', user_update, name="user_update"),
    url(r'^testmap$', test, name="testmap"),
    url(r'^friend_add/(?P<slug>[-\w]+)$', friend_add, name="friend_add"),
    url(r'^friend_delete/(?P<slug>[-\w]+)$', friend_delete, name="friend_delete"),
    # url(r'^group_create$', CreateView.as_view(model=GroupProfile,
    #                                           template_name="group_create.html",
    #                                           success_url='group_detail'),
    #     name="group_create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
