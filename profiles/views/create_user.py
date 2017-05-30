from django.shortcuts import render, reverse, HttpResponseRedirect
from profiles.forms import Form_register, Form_login
from profiles.models import UserProfile, Invite
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def page(request):
    form = Form_register(prefix='register')
    form_log = Form_login(prefix='login')
    context = {
        "form": form,
        "form_log": form_log,
    }
    if request.method == 'POST' and 'login' in request.POST:
        form_log = Form_login(request.POST, prefix='login')
        if form_log.is_valid():
            username = form_log.cleaned_data["username"]
            password = form_log.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                from django.contrib.auth import login
                login(request, user)
            if request.user.is_authenticated():
                profile = UserProfile.objects.get(user_auth=request.user)
                context['profile'] = profile
                frequests = Invite.objects.filter(r_to=profile).exclude(r_from=profile)
                context['frequests'] = frequests
            return render(request, "welcome.html", context)

    if request.method == 'POST' and 'register' in request.POST:
        form = Form_register(request.POST, prefix='register')
        if form.is_valid():
            # name = form.cleaned_data['name']
            # last_name = form.cleaned_data['last_name']
            login = form.cleaned_data['login'].lower()
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user_auth = User.objects.create_user(username=login, email=email, password=password)
            user_auth.is_active = True
            # user_auth.first_name = name
            # user_auth.last_name = last_name

            user_auth.save()
            new_user = UserProfile(user_auth=user_auth)
            new_user.save()
            user = authenticate(username=login, password=password)
            if user:
                from django.contrib.auth import login
                login(request, user)
            return HttpResponseRedirect(reverse('welcome'))
        else:
            if request.user.is_authenticated():
                profile = UserProfile.objects.get(user_auth=request.user)
                context['profile'] = profile
                frequests = Invite.objects.filter(r_to=profile).exclude(r_from=profile)
                context['frequests'] = frequests
            return render(request, 'welcome.html', context)

    if request.user.is_authenticated():
        profile = UserProfile.objects.get(user_auth=request.user)
        context['profile'] = profile
        frequests = Invite.objects.filter(r_to=profile).exclude(r_from=profile)
        context['frequests'] = frequests

    return render(request, "welcome.html", context)
