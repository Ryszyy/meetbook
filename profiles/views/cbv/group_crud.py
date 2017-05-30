from profiles.models import GroupProfile, UserProfile
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView

import datetime
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class GroupsList(ListView):
    model = GroupProfile
    template_name = 'groups_list.html'
    context_object_name = 'groups_list'

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)
        context['profile'] = profile
        return context


class GroupDetailView(DetailView):
    model = GroupProfile
    template_name = 'group_detail.html'


class Form_Group(forms.Form):
    name = forms.CharField(label="Name", max_length=120)
    intrest = forms.CharField(label="Intrest")


def group_create(request):

    if request.POST:
        form = Form_Group(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            intrest = form.cleaned_data['intrest']

            user = UserProfile.objects.get(user_auth=request.user)

            new_intrest, create = Intrest.objects.get_or_create(name=intrest)

            new_event = Group(name=name, owner=user, intrest=new_intrest)
            new_event.save()
            new_event.members.add(user)

            return HttpResponseRedirect(reverse('event_detail', args=[new_event.slug]))
        else:
            return render(request, 'event_create.html', {'form': form})
    else:
        form = Form_Group()
    form = Form_Group()
    return render(request, 'event_create.html', {'form': form})
