from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def pin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('pin_verified'):
            request.session['next_after_pin'] = request.path
            return redirect('app:verify_pin')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='app:login')
def verify_pin(request):
    profile = getattr(request.user, 'profile', None)

    context = {
        'profile':    profile,
        'first_name': request.user.first_name or request.user.username,
        'full_name':  request.user.get_full_name() or request.user.username,
    }

    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()

        if profile and profile.check_pin(pin):
            request.session['pin_verified'] = True
            next_url = request.session.pop('next_after_pin', None)
            return redirect(next_url or 'app:domestic_transfer')

        messages.error(request, 'Incorrect PIN. Please try again.')
        return render(request, 'app/verify_pin.html', context)

    return render(request, 'app/verify_pin.html', context)