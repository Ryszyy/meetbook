from profile.models import UserProfile


def friends_list(request):
    return{
        'friends': UserProfile.objects.filter(user_auth=request.user)
    }


def groups_list(request):
    return{
        'groups': UserProfile.objects.filter(user_auth=request.user)
    }


def get_current_path(request):
    return {
        'current_path': request.get_full_path().split('.')[:-1]
    }
