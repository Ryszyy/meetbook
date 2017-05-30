from django.shortcuts import render, reverse, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile, Invite


@login_required
def friend_add(request, slug):
    profile = UserProfile.objects.get(user_auth=request.user)
    # sent = Invite.objects.filter(r_from=request.user)

    other = UserProfile.objects.get(slug=slug)
    try:
        recived = Invite.objects.get(r_from=other, r_to=profile)
    except Invite.DoesNotExist:
        recived = None

    if request.method == 'POST':
        if recived:
            profile.friends.add(recived.r_from)
            recived.delete()
        else:
            try:
                r_to = Invite(r_from=profile, r_to=other)
                r_to.save()
            except:
                pass
        return HttpResponseRedirect(reverse('users_list'))
    else:
        return HttpResponse('You have no permissions to enter that site this way')


@login_required
def friend_delete(request, slug):
    poor_guy = UserProfile.objects.get(slug=slug)
    me_guy = UserProfile.objects.get(user_auth=request.user)
    context = {
        "Title": "Do you want to remove your friend?",
        "Confirmation": "Remove",
    }

    if poor_guy in me_guy.friends.all():
        if request.method == 'POST':
            try:
                me_guy.friends.remove(poor_guy)
                return HttpResponseRedirect(reverse('users_list'))
            except:
                pass
        return render(request, 'delete.html', context)
    else:
        return HttpResponse("Can't be done")
