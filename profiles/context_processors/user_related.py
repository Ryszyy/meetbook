from profile.models import UserProfile


def friends_list(request):
    return{
        'friends': UserProfile.objects.filter(user_auth=request.user)
    }
