from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from functools import wraps

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # You can either render a template
            return render(request, 'login_required.html', {
                'message': 'You need to login to access this page.'
            }, status=403)
            
            # Or return a simple HTTP response
            # return HttpResponse('You need to login to access this page.', status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper