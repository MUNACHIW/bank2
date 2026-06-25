# Add these to your views.py

from functools import wraps
from django.contrib import messages
from django.shortcuts import  redirect


# ============================================================
# DECORATOR - require a verified PIN before sensitive actions
# Usage: stack this UNDER @login_required on transfer views
# ============================================================
def pin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)

        # If user has no PIN set yet, force them to set one first
        if not profile or not profile.has_pin:
            messages.info(request, "Please set up your transaction PIN to continue.")
            request.session['next_after_pin'] = request.path
            return redirect('app:set_pin')

        # If PIN not verified for this session, redirect to verify page
        if not request.session.get('pin_verified'):
            request.session['next_after_pin'] = request.path
            return redirect('app:verify_pin')

        return view_func(request, *args, **kwargs)
    return wrapper


# ============================================================
# SET PIN - shown once, first time user tries a sensitive action
# ============================================================
