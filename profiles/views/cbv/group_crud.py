from profiles.models import GroupProfile, UserProfile, Intrest, FreeTime, Event, Location
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.forms import ModelForm, Textarea
from django.db.models import Q
import datetime
from django import forms
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse, redirect
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class GroupsList(ListView):
    model = GroupProfile
    template_name = 'groups_list.html'
    context_object_name = 'groups_list'

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)

        created_groups = GroupProfile.objects.filter(owner=profile)
        member_of_group = GroupProfile.objects.filter(members=profile).exclude(owner=profile)
        groups = GroupProfile.objects.all().exclude(members=profile).exclude(owner=profile)

        context['groups_list'] = groups
        context['member_of_group'] = member_of_group
        context['created_groups'] = created_groups
        context['profile'] = profile
        return context


class GroupDetailView(DetailView):
    model = GroupProfile
    template_name = 'group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)
        slug = self.request.path.split('/')[-1]
        group = GroupProfile.objects.get(slug=slug)
        u_time = FreeTime.objects.filter(group=group, user=profile).order_by('start_date')
        try:
            group_event = Event.objects.get(group=group)
            context['event'] = group_event
        except Exception as e:
            print(str(e) + " group dont have any events")

        try:
            from_user=group.message.split("\nfrom - ")[-1]
            for member in group.members.all():
                if str(member) == from_user:
                    group.message = ""
                    group.save()
                    context = super(GroupDetailView, self).get_context_data(**kwargs)
        except:
            pass


        all_time = FreeTime.objects.filter(end_date__lt=timezone.now().replace(tzinfo=None))
        all_time.delete()


        context['profile'] = profile
        context['u_time'] = u_time
        return context


class Form_Group(forms.Form):
    name = forms.CharField(label="Name", max_length=120)
    intrest = forms.CharField(label="Intrest")

    def clean(self):
        cleaned_data = super(Form_Group, self).clean()
        name = self.cleaned_data.get('name')
        intrest = self.cleaned_data.get('intrest')

        if GroupProfile.objects.filter(name=name):
            raise forms.ValidationError("Name is already taken")


        return self.cleaned_data

def group_create(request):

    if request.POST:
        form = Form_Group(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            intrest = form.cleaned_data['intrest']

            user = UserProfile.objects.get(user_auth=request.user)

            new_intrest, create = Intrest.objects.get_or_create(name=intrest)

            new_group = GroupProfile(name=name, owner=user)
            new_group.save()
            new_group.intrest.add(new_intrest)
            new_group.members.add(user)

            return HttpResponseRedirect(reverse('group_detail', args=[new_group.slug]))
        else:
            return render(request, 'group_create.html', {'form': form})
    form = Form_Group()
    return render(request, 'group_create.html', {'form': form})


@login_required
def group_delete(request, slug):
    profile = UserProfile.objects.get(user_auth=request.user)
    group = GroupProfile.objects.get(slug=slug)

    if profile == group.owner:
        context = {
            "Title": "Do you want to delete the event?",
            "Confirmation": "Delete",
        }

        if request.method == 'POST':
            poor_group = GroupProfile.objects.get(slug=slug)
            poor_group.delete()
            return HttpResponseRedirect(reverse('groups_list'))
        return render(request, 'delete.html', context)
    else:
        return HttpResponse('You have no permissions to enter that site')


class FormUpdateMember(ModelForm):
    class Meta:
        model = GroupProfile
        fields = ['members']


class GMemberUpdate(UpdateView, LoginRequiredMixin):
    model = GroupProfile
    template_name = 'members_manager.html'
    form_class = FormUpdateMember

    def get_success_url(self, **kwargs):
        slug = self.request.path.split('/')[-1]
        return (reverse('group_detail', args=[slug]))



def date_add(request, slug):
    if request.method == 'POST':
        date_start = request.POST['date_start']
        date_end = request.POST['date_end']
        datetime_object_start = timezone.now().replace(tzinfo=None)
        datetime_object_end = timezone.now().replace(tzinfo=None)
        # print("date is - " + str(datetime_object_start))

        try:
            try:
                date = date_start.replace("/", "-")
                datetime_object_start = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
                # print("date is - " + str(datetime_object_start))
                if datetime_object_start < timezone.now().replace(tzinfo=None):
                    mess = "You can't assign your free time to the past"
                    # raise forms.ValidationError("You can't create event in the past")
                    return render(request, 'date_add.html', {"messages":mess})
            except ValueError:
                mess = "Provide correct values"
                return render(request, 'date_add.html', {"messages":mess})

            try:
                date = date_end.replace("/", "-")
                datetime_object_end = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
                if datetime_object_end < datetime_object_start:
                    mess = "End of your free time should be after it start's"
                    # raise forms.ValidationError("You can't create event in the past")
                    return render(request, 'date_add.html', {"messages":mess})
            except ValueError:
                mess = "Provide correct values"
                return render(request, 'date_add.html', {"messages":mess})


        except Exception as e:
            # print(e)
            return render(request, 'date_add.html', {})
        else:
            group = GroupProfile.objects.get(slug=slug)
            user = UserProfile.objects.get(user_auth=request.user) 
            new_date = FreeTime(start_date=datetime_object_start,
                                end_date=datetime_object_end,
                                group=group,
                                user=user
             )
            new_date.save()
            user.time.add(new_date)

            # extract all dates from all users within group
            
            times = FreeTime.objects.filter(
                group=group,
                start_date__lte=timezone.now() + timedelta(hours=20),
                end_date__lte=timezone.now() + timedelta(hours=20)
                )
            start_list = []
            end_list = []
            for time in times:
                end_list.append(time.end_date)
                start_list.append(time.start_date)

            #find latest startdate


            try:
                latest_start = max(start_list)
            except:
                pass
            error = False
            for end in end_list:
                if latest_start < end:
                    continue
                else:
                    error=True
                    break
            if not error:
                try:
                    group.date = (latest_start)
                    group.save()
                except:
                    pass



            return redirect('group_detail', slug=slug)
    return render(request, 'date_add.html', {})


class Form_Group_Event(forms.Form):
    name = forms.CharField(label="Name", max_length=120)


    def clean(self):
        cleaned_data = super(Form_Group_Event, self).clean()
        return self.cleaned_data


def group_event_create(request, slug):
    profile = UserProfile.objects.get(user_auth=request.user)
    context = {
        "profile": profile
    }
    if request.method == 'POST':
        location_in = request.POST['location_in']
        if request.POST['latitude'] == "" or request.POST['longitude'] == "" or request.POST['location_map'] == "":
            mess = "Choose your location"
            context["message"] = mess
            return render(request, 'group_event_create.html', context)
        else:
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            location_map = request.POST['location_map']
            form = Form_Group_Event(request.POST)
            location =location_map.split(',')[-2:]
            location = ",".join(location)
            if form.is_valid():
                name = form.cleaned_data['name']
                new_loc_obj, create = Location.objects.get_or_create(
                    city=location,
                    latitude=latitude,
                    longitude=longitude)


                group = GroupProfile.objects.get(slug=slug)
                try:
                    old_event = Event.objects.get(group=group)
                    old_event.delete()
                except:
                    pass
                intrest = Intrest.objects.get(name=group.intrest.all()[:1].get())
                new_event = Event(
                    name=name,
                    date=group.date,
                    location=new_loc_obj,
                    intrest=intrest,
                    creator=profile,
                    group=group
                    )
                new_event.save()

                # new_event.location.add(new_loc_obj)

                for member in group.members.all():
                    m = UserProfile.objects.get(user_auth=member)
                    new_event.members.add(m)

                return redirect('group_detail', slug=slug)

            form = Form_Group_Event()
            context["form"] = form
            return render(request, 'group_event_create.html', context)
    form = Form_Group_Event()
    context["form"] = form
    return render(request, 'group_event_create.html', context)

class EventGroupDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_group.html'

    def get_context_data(self, **kwargs):
        context = super(EventGroupDetailView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(user_auth=self.request.user)

        slug = self.request.path.split('/')[-1]
        event = Event.objects.get(slug=slug)

        now = timezone.now() + timedelta(hours=1)
        time = event.date > now
        context['profile'] = profile
        context['time'] = time
        
        return context


class Form_Message(forms.Form):
    message = forms.CharField(label="Message", max_length=1000,  widget=forms.Textarea)


def message_creator(request, slug):
    if request.method == 'POST':
        form = Form_Message(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            if request.user.first_name != "":
                m_from = f"\nfrom - {request.user.first_name} {request.user.last_name}"
            else:
                m_from = f"\nfrom - {request.user}"
            
            message = message + m_from
            group = GroupProfile.objects.get(slug=slug)
            group.message = message
            group.save()
            return redirect('group_detail', slug=slug)
        form = Form_Group_Event()
        return render(request, 'send_message.html', {"form":form})
    form = Form_Message() 
    return render(request, 'send_message.html', {"form":form})