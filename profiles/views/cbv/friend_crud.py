from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def friend_add(request, slug):
    return render(request, 'friend_add.html', {})


@login_required
def friend_delete(request, slug):
    return render(request, 'friend_delete.html', {})
