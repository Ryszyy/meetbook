from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from profiles.models import UserProfile, Location, Invite
from django.shortcuts import render, redirect, reverse
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
        slug = self.request.path.split('/')[-1]
        context.update({'param': slug})
        try:
            other = UserProfile.objects.get(slug=slug)
            req_sent = Invite.objects.get(r_from=profile, r_to=other)
            context['req_sent'] = req_sent
        except Invite.DoesNotExist:
            req_sent = None

        return context


class UsersList(ListView):
    model = UserProfile
    template_name = 'users_list.html'
    context_object_name = 'users_list'

    def get_context_data(self, **kwargs):
        context = super(UsersList, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)
        context['profile'] = profile

        # pending = Invite.objects.filter(r_to=profile)

        req_sent = Invite.objects.filter(r_from=profile)

        context['req_sent'] = req_sent
        users_list = UserProfile.objects.all()
        for f in profile.friends.all():
            users_list = users_list.exclude(user_auth=f)
        users_list = users_list.exclude(user_auth=self.request.user)
        for f in req_sent:
            other = f.r_to
            users_list = users_list.exclude(user_auth=other)

        context['users_list'] = users_list
        return context


@login_required
def user_delete(request, slug):
    profile = UserProfile.objects.get(user_auth=request.user)
    if profile.slug == slug:
        context = {
            "Title": "Do you want to delete your account?",
            "Confirmation": "Delete",
        }
        if request.method == 'POST':
            user_ad = request.user
            user_ad.delete()
            logout(request)
            return redirect('welcome')
        return render(request, 'delete.html', context)
    else:
        return HttpResponse('You have no permissions to enter that site')


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
