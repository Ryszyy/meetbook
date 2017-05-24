from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from profiles.models import UserProfile, Location
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from profiles.forms import Form_update_user, Form_update_user_later

from django.contrib.auth.models import User


class UserDetailView(DetailView):
    model = UserProfile
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)
        context['profile'] = profile
        context.update({'param': self.request.path.split('/')[-1]})
        return context


class UsersList(ListView):
    model = UserProfile
    template_name = 'users_list.html'
    context_object_name = 'users_list'

    def get_context_data(self, **kwargs):
        context = super(UsersList, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)
        context['profile'] = profile
        users_list = UserProfile.objects.exclude(friends__in=profile.friends.all())
        context['users_list'] = users_list
        return context


@login_required
def user_delete(request, slug):
    if request.user.username == slug:
        if request.method == 'POST':
            user_ad = request.user
            user_ad.delete()
            logout(request)
            return render(request, 'user_delete.html', {})
        return render(request, 'user_delete.html', {})
    else:
        return HttpResponse('You have not permissions to do that')


@login_required
def user_update(request, slug):
    if request.user.username == slug:
        if not (request.user.first_name == '' or request.user.last_name == ''):
            if request.method == 'POST':
                profile = UserProfile.objects.get(user_auth=request.user)
                form = Form_update_user_later(request.POST, request.FILES, initial={'bio': profile.bio, 'location': profile.location, 'picture': profile.picture})
                if form.is_valid():
                    bio = form.cleaned_data['bio']
                    location = form.cleaned_data['location']
                    picture = form.cleaned_data['picture']
                    local, created = Location.objects.get_or_create(city=location)
                    local.save()
                    profile.bio = bio
                    profile.location = local
                    profile.picture = picture
                    profile.save()

                    return redirect('user_detail', slug=request.user)
                context = {
                    "form": form,
                }
                return render(request, 'user_update.html', context)
            profile = UserProfile.objects.get(user_auth=request.user)
            form = Form_update_user_later(initial={'bio': profile.bio,
                                                   'location': profile.location,
                                                   'picture': profile.picture})
            return render(request, 'user_update.html', {'form': form})

        else:
            if request.method == 'POST':
                profile = UserProfile.objects.get(user_auth=request.user)
                form = Form_update_user(request.POST, request.FILES)
                if form.is_valid():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    bio = form.cleaned_data['bio']
                    location = form.cleaned_data['location']
                    picture = form.cleaned_data['picture']
                    user_auth = User.objects.get(username=request.user.username)
                    user_auth.first_name = first_name
                    user_auth.last_name = last_name
                    user_auth.save()
                    local, created = Location.objects.get_or_create(city=location)
                    local.save()

                    profile.bio = bio
                    profile.location = local
                    profile.picture = picture
                    profile.save()

                    return redirect('user_detail', slug=request.user)
                context = {
                    "form": form,
                }
                return render(request, 'user_update.html', context)
            form = Form_update_user()
            return render(request, 'user_update.html', {'form': form})
    else:
        return HttpResponse('You have not permissions to do that')


@login_required
def test(request):
    return render(request, 'testmap.html', {"msg": "mesydż"})
