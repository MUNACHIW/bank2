from django.shortcuts import redirect
from django.contrib.auth import logout


class AccountActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile and not profile.is_active:
                logout(request)
                # Pass flag via session so signin page shows popup
                request.session['account_disabled'] = True
                return redirect('bank:signin')

        return self.get_response(request)