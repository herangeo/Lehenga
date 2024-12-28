from django.contrib.auth.models import User
from .models import Cart


def user_context(request):
    return {
        'username': request.user.username if request.user.is_authenticated else None,
    }


def cart_count(request):
    if request.user.is_authenticated:  # Check if user is logged in
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'cart_count': cart.items.count()}  # Return the count of cart items
    else:
        return {'cart_count': 0}

