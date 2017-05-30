from profiles.models import Event, UserProfile, Location, Intrest
from django.views.generic.list import ListView
import datetime
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from braces.views import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


class Form_Event(forms.Form):
    name = forms.CharField(label="Name", max_length=120)
    location = forms.CharField(label="Location")
    date = forms.DateTimeField(label="Date", widget=forms.SelectDateWidget())
    intrest = forms.CharField(label="Intrest")

    def clean(self):
        cleaned_data = super(Form_Event, self).clean()
        return self.cleaned_data


def event_create(request):

    if request.POST:
        form = Form_Event(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            date = form.cleaned_data['date']
            intrest = form.cleaned_data['intrest']

            user = UserProfile.objects.get(user_auth=request.user)
            new_location, create = Location.objects.get_or_create(city=location)
            new_intrest, create = Intrest.objects.get_or_create(name=intrest)

            new_event = Event(name=name, creator=user, location=new_location, date=date, intrest=new_intrest)
            new_event.save()
            new_event.members.add(user)

            return HttpResponseRedirect(reverse('event_detail', args=[new_event.slug]))
        else:
            return render(request, 'event_create.html', {'form': form})
    else:
        form = Form_Event()
    form = Form_Event()
    return render(request, 'event_create.html', {'form': form})


class EventsList(ListView):
    model = Event
    template_name = 'events_list.html'
    context_object_name = 'events_list'

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)

        my_events = Event.objects.filter(members=profile)
        events = Event.objects.filter(date__gte=datetime.datetime.now() - datetime.timedelta(days=1)).exclude(members=profile)
        # events = events.exclude(my_events)

        context['profile'] = profile
        context['events_list'] = events
        context['my_events'] = my_events
        return context


class PastEventsList(ListView):
    model = Event
    template_name = 'past_events.html'
    context_object_name = 'events_list'

    def get_context_data(self, **kwargs):
        context = super(PastEventsList, self).get_context_data(**kwargs)
        events = Event.objects.filter(date__lte=datetime.date.fromordinal(datetime.date.today().toordinal() - 1))
        context['events_list'] = events
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)
        slug = self.request.path.split('/')[-1]
        event = Event.objects.get(slug=slug)

        now = timezone.now()
        time = event.date > now
        context['profile'] = profile
        context['time'] = time
        return context


@login_required
def event_join(request, slug):
    profile = UserProfile.objects.get(user_auth=request.user)
    event = Event.objects.get(slug=slug)

    if request.method == 'POST':
        try:
            event.members.add(profile)
        except:
            pass
    return HttpResponseRedirect(reverse('event_detail', args=[event.slug]))


@login_required
def event_delete(request, slug):
    profile = UserProfile.objects.get(user_auth=request.user)
    if profile.slug == slug:
        context = {
            "Title": "Do you want to delete the event?",
            "Confirmation": "Delete",
        }

        if request.method == 'POST':
            poor_event = Event.objects.get(slug=slug)
            poor_event.delete()
            return HttpResponseRedirect(reverse('events_list'))
        return render(request, 'delete.html', context)
    else:
        return HttpResponse('You have no permissions to enter that site')


@login_required
def member_delete(request, slug):
    event = Event.objects.get(slug=slug)
    owner = event.owner
    if request.user == owner.user_auth:
        pass
    return HttpResponseRedirect(reverse('event_detail', args=[slug]))
