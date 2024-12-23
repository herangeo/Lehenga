from django.contrib.auth.models import User

def user_context(request):
    return {
        'username': request.user.username if request.user.is_authenticated else None,
    }
