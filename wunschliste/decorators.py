from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages


def simple_auth_required(username_setting, password_setting, login_url_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get(f'auth_{username_setting}'):
                return view_func(request, *args, **kwargs)
            
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                
                if (username == getattr(settings, username_setting) and 
                    password == getattr(settings, password_setting)):
                    request.session[f'auth_{username_setting}'] = True
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'Falsche Zugangsdaten!')
            
            return redirect(login_url_name)
        
        return _wrapped_view
    return decorator