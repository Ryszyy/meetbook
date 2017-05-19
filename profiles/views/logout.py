from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import logout
from profiles.forms import Form_register, Form_login


def page(request):
    logout(request)
    form = Form_register()
    form_log = Form_login()
    return HttpResponseRedirect(reverse('welcome'))
