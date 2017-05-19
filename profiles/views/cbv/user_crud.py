from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from profiles.models import UserProfile
from django.shortcuts import render
from django.contrib.auth import logout


class UserDetailView(DetailView):
    model = UserProfile
    template_name = 'user_detail.html'


class UsersList(ListView):
    model = UserProfile
    template_name = 'users_list.html'
    context_object_name = 'users_list'

    def get_context_data(self, **kwargs):
        context = super(UsersList, self).get_context_data(**kwargs)

        return context


def user_delete(request, slug):
    user_ad = request.user
    user_ad.delete()
    logout(request)
    return render(request, 'user_delete.html', {})


def user_update(request, slug):
    user_u = UserProfile.objects.get(slug=slug)
    print(user_u)
    context = {
        "user_u": user_u,
    }
    return render(request, 'user_update.html', context)


def test(request):
    return render(request, 'test.html', {"msg": "mesydż"})
