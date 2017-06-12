from profiles.models import Event, UserProfile, Location, Intrest
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from datetime import timezone, timedelta
import datetime
from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse, redirect
from braces.views import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class Form_Event(forms.Form):
    name = forms.CharField(label="Name", max_length=120)
    intrest = forms.CharField(label="Intrest")
    cost = forms.IntegerField(label="Cost (PLN)")

    def clean(self):
        cleaned_data = super(Form_Event, self).clean()
        return self.cleaned_data



def event_create(request):
    context = {}
    if request.method == "POST": 
        location_in = request.POST['location_in']
        if request.POST['latitude'] == "" or request.POST['longitude'] == "" or request.POST['location_map'] == "":
            mess = "Choose your location"
            context["message"] = mess
            return render(request, 'event_create.html', context)

        form = Form_Event(request.POST)
        date_form = request.POST['date']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location_map = request.POST['location_map']
        location =location_map.split(',')[-2:]
        location = ",".join(location)
        if form.is_valid():
            name = form.cleaned_data['name']
            intrest = form.cleaned_data['intrest']
            cost = form.cleaned_data['cost']
            try:
                date = date_form.replace("/", "-")
                datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
                if datetime_object < timezone.now().replace(tzinfo=None):
                    mess = "You can't create event in the past"
                    # raise forms.ValidationError("You can't create event in the past")
                    return render(request, 'event_create.html', {'form': form, "messages":mess})
            except ValueError:
                mess = "Double check if date is correct"
                return render(request, 'event_create.html', {'form': form, "messages":mess})



            user = UserProfile.objects.get(user_auth=request.user)
            new_loc_obj, create = Location.objects.get_or_create(
                    city=location,
                    latitude=latitude,
                    longitude=longitude)
            new_intrest, create = Intrest.objects.get_or_create(name=intrest)

            new_event = Event(name=name, creator=user, location=new_loc_obj, date=datetime_object, intrest=new_intrest, cost=cost)
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


        created_events = Event.objects.filter(Q(creator=profile), Q(group=None) , Q(date__gte=datetime.datetime.now() - datetime.timedelta(days=3))).order_by('date')
        member_of_event = Event.objects.filter(Q(members=profile), Q(group=None) , Q(date__gte=datetime.datetime.now() - datetime.timedelta(days=3))).exclude(creator=profile).order_by('date')
        events = Event.objects.filter(Q(group=None), Q(date__gte=datetime.datetime.now() - datetime.timedelta(days=3))).exclude(members=profile).exclude(creator=profile).order_by('date')


        context['events_list'] = events
        context['member_of_event'] = member_of_event
        context['created_events'] = created_events
        context['profile'] = profile
        return context


class PastEventsList(ListView):
    model = Event
    template_name = 'past_events.html'
    context_object_name = 'events_list'

    def get_context_data(self, **kwargs):
        context = super(PastEventsList, self).get_context_data(**kwargs)
        
        profile = UserProfile.objects.get(user_auth=self.request.user)
        events = Event.objects.filter(date__lte=datetime.date.fromordinal(datetime.date.today().toordinal() - 3)).exclude(members=profile).exclude(creator=profile).order_by('date')

        created_events = Event.objects.filter(Q(creator=profile) , Q(date__lte=datetime.date.fromordinal(datetime.date.today().toordinal() - 3))).order_by('date')
        member_of_event = Event.objects.filter(Q(members=profile) , Q(date__lte=datetime.date.fromordinal(datetime.date.today().toordinal() - 3))).exclude(creator=profile).order_by('date')
        


        context['events_list'] = events
        context['member_of_event'] = member_of_event
        context['profile'] = profile
        context['created_events'] = created_events
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)

        slug = self.request.path.split('/')[-1]
        event = Event.objects.get(slug=slug)

        now = timezone.now() + timedelta(hours=1)
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
    event = Event.objects.get(slug=slug)

    if profile == event.creator:
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
    new_user = UserProfile.objects.get(user_auth=request.user)
    if new_user in event.members.all():
        context = {
            "Title": "Do you want to resign?",
            "Confirmation": "Resign",
        }
        if request.method == 'POST':
            event.members.remove(new_user)
            return HttpResponseRedirect(reverse('event_detail', args=[slug]))
        return render(request, 'delete.html', context)
    else:
        return HttpResponse('You have no permissions to enter that site')


@login_required
def event_update(request, slug):
    event = Event.objects.get(slug=slug)
    context = {"event":event}
    if event.creator.user_auth == request.user:
        if request.method == 'POST':
            date_form = request.POST['date']
            try:
                date = date_form.replace("/", "-")
                datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
                if datetime_object < timezone.now().replace(tzinfo=None):
                    mess = "You can't create event in the past"
                    context["messages"]=mess
                    # raise forms.ValidationError("You can't create event in the past")
                    return render(request, 'event_update.html', context)
            except ValueError:
                mess = "Choose your Date"
                context["messages"]=mess
                return render(request, 'event_update.html', context)
            else:
                event.date = date
                event.save()
            location_in = request.POST['location_in']
            if request.POST['latitude'] == "" or request.POST['longitude'] == "" or request.POST['location_map'] == "":
                mess = "Choose your location"
                context["messages"] = mess
                return render(request, 'event_update.html', context)
            else: 
                latitude = request.POST['latitude']
                longitude = request.POST['longitude']
                location_map = request.POST['location_map']
                location =location_map.split(',')[-2:]
                location = ",".join(location)
                new_loc_obj, create = Location.objects.get_or_create(
                    city=location,
                    latitude=latitude,
                    longitude=longitude)   
                event.location = new_loc_obj
                event.save()
                return redirect('event_detail', slug=event.slug)
        return render(request, 'event_update.html', context)
    else:
        return HttpResponse('You have no permissions to enter that site')


class FormUpdateMember(ModelForm):
    class Meta:
        model = Event
        fields = ['members']


class EMemberUpdate(UpdateView, LoginRequiredMixin):
    model = Event
    template_name = 'members_manager.html'
    form_class = FormUpdateMember

    def get_success_url(self, **kwargs):
        slug = self.request.path.split('/')[-1]
        return (reverse('event_detail', args=[slug]))