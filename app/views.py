from django.shortcuts import render, redirect ,  get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count
from datetime import date, timedelta
from .models import   WireTransfer, DomesticTransfer , LoanApplication ,Deposit,  Notification
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator
from decimal import Decimal


User = get_user_model()
# Create your views here.
def landing(request):
    return render(request, "app/index.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # use Django’s login
            messages.success(request, "Welcome back! You are now signed in.")
            return redirect("app:dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "app/login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":

        first_name = request.POST.get("firstName")
        middle_name = request.POST.get("middleName")
        last_name = request.POST.get("lastName")
        username = request.POST.get("username")

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        country = request.POST.get("country")

        account_type = request.POST.get("accountType")
        currency = request.POST.get("currency")

        pin = request.POST.get("pin")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("/signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("/signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("/signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.middle_name = middle_name
        user.phone = phone
        user.country = country
        user.account_type = account_type
        user.currency = currency
        user.pin = pin

        user.save()

        messages.success(request, "Account created successfully.")

        return redirect("/login")

    return render(request, "app/signup.html")


@login_required(login_url="app:login")
def dashboard(request):
    profile = getattr(request.user, "profile", None)
    initial_balance = profile.initial_balance if profile else Decimal("0.00")

    wire_transfers = WireTransfer.objects.filter(user=request.user).order_by('-created_at')[:3]
    domestic_transfers = DomesticTransfer.objects.filter(user=request.user).order_by('-created_at')[:3]

    all_transfers = sorted(
        chain(wire_transfers, domestic_transfers),
        key=attrgetter('created_at'),
        reverse=True
    )[:3]

    # --- Chart data: last 7 days ---
    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    labels = [d.strftime('%a') for d in last_7_days]  # Mon, Tue...

    # Get daily totals for wire transfers
    wire_daily = (
        WireTransfer.objects
        .filter(user=request.user, created_at__date__gte=last_7_days[0])
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('amount'))
    )
    domestic_daily = (
        DomesticTransfer.objects
        .filter(user=request.user, created_at__date__gte=last_7_days[0])
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('amount'))
    )

    # Map to dict for quick lookup
    wire_map     = {str(item['day']): float(item['total']) for item in wire_daily}
    domestic_map = {str(item['day']): float(item['total']) for item in domestic_daily}

    # Build chart arrays matching last_7_days order
    chart_wire     = [wire_map.get(str(d), 0) for d in last_7_days]
    chart_domestic = [domestic_map.get(str(d), 0) for d in last_7_days]
    chart_total    = [wire_map.get(str(d), 0) + domestic_map.get(str(d), 0) for d in last_7_days]

    import json
    context = {
        "profile":          profile,
        "balance_display":  f"{initial_balance:,.2f}",
        "currency_display": profile.currency if profile else "USD",
        "full_name":        request.user.get_full_name() or request.user.username,
        "first_name":       request.user.first_name or request.user.username,
        "transactions":     all_transfers,
        "chart_labels":     json.dumps(labels),
        "chart_wire":       json.dumps(chart_wire),
        "chart_domestic":   json.dumps(chart_domestic),
        "chart_total":      json.dumps(chart_total),
    }
    return render(request, "app/dashboard.html", context)





@login_required(login_url='bank:signin')
def wire_transfer(request):
    profile = getattr(request.user, 'profile', None)
 
    if request.method == 'POST':
        amount                 = request.POST.get('amount', '').strip()
        beneficiary_name       = request.POST.get('beneficiary_name', '').strip()
        beneficiary_account_no = request.POST.get('beneficiary_account_no', '').strip()
        bank_name              = request.POST.get('bank_name', '').strip()
        country                = request.POST.get('country', '').strip()
        swift_code             = request.POST.get('swift_code', '').strip()
        routing_number         = request.POST.get('routing_number', '').strip()
        account_type           = request.POST.get('account_type', '').strip()
        narration              = request.POST.get('narration', '').strip()
 
        if not all([amount, beneficiary_name, beneficiary_account_no, bank_name, country, swift_code]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'app/wire_transfer.html', {'profile': profile})
 
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Please enter a valid amount.')
            return render(request, 'app/wire_transfer.html', {'profile': profile})
 
        transfer = WireTransfer.objects.create(
            user=request.user,
            amount=amount,
            beneficiary_name=beneficiary_name,
            beneficiary_account_no=beneficiary_account_no,
            bank_name=bank_name,
            country=country,
            swift_code=swift_code,
            routing_number=routing_number,
            account_type=account_type,
            narration=narration,
            status='Pending',
        )
 
        # Redirect to receipt page
        return redirect('app:transfer_receipt', transfer_type='wire', transfer_id=transfer.id)
 
    return render(request, 'app/wire_transfer.html', {'profile': profile})
 
 
@login_required(login_url='app:login')
def domestic_transfer(request):
    profile = getattr(request.user, 'profile', None)
 
    if request.method == 'POST':
        amount                 = request.POST.get('amount', '').strip()
        beneficiary_name       = request.POST.get('beneficiary_name', '').strip()
        beneficiary_account_no = request.POST.get('beneficiary_account_no', '').strip()
        bank_name              = request.POST.get('bank_name', '').strip()
        account_type           = request.POST.get('account_type', '').strip()
        narration              = request.POST.get('narration', '').strip()
 
        if not all([amount, beneficiary_name, beneficiary_account_no, bank_name]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'app/domestic_transfer.html', {'profile': profile})
 
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Please enter a valid amount.')
            return render(request, 'app/domestic_transfer.html', {'profile': profile})
 
        transfer = DomesticTransfer.objects.create(
            user=request.user,
            amount=amount,
            beneficiary_name=beneficiary_name,
            beneficiary_account_no=beneficiary_account_no,
            bank_name=bank_name,
            account_type=account_type,
            narration=narration,
            status='Pending',
        )
 
        # Redirect to receipt page
        return redirect('app:transfer_receipt', transfer_type='domestic', transfer_id=transfer.id)
 
    return render(request, 'app/domestic_transfer.html', {'profile': profile})


@login_required(login_url='app:login')
def transactions(request):
    profile = getattr(request.user, 'profile', None)
    active_filter = request.GET.get('filter', 'all')
    search_query  = request.GET.get('q', '').strip()
 
    # --- Fetch both transfer types ---
    wire_qs     = WireTransfer.objects.filter(user=request.user)
    domestic_qs = DomesticTransfer.objects.filter(user=request.user)
 
    # --- Apply status filters ---
    if active_filter == 'wire':
        wire_qs     = wire_qs
        domestic_qs = domestic_qs.none()
    elif active_filter == 'domestic':
        wire_qs     = wire_qs.none()
        domestic_qs = domestic_qs
    elif active_filter == 'pending':
        wire_qs     = wire_qs.filter(status='Pending')
        domestic_qs = domestic_qs.filter(status='Pending')
    elif active_filter == 'completed':
        wire_qs     = wire_qs.filter(status='Completed')
        domestic_qs = domestic_qs.filter(status='Completed')
    elif active_filter == 'failed':
        wire_qs     = wire_qs.filter(status='Failed')
        domestic_qs = domestic_qs.filter(status='Failed')
 
    # --- Apply search ---
    if search_query:
        wire_qs     = wire_qs.filter(beneficiary_name__icontains=search_query) | \
                      wire_qs.filter(bank_name__icontains=search_query)
        domestic_qs = domestic_qs.filter(beneficiary_name__icontains=search_query) | \
                      domestic_qs.filter(bank_name__icontains=search_query)
 
    # --- Tag each record with its transfer type ---
    wire_list     = list(wire_qs)
    domestic_list = list(domestic_qs)
 
    for txn in wire_list:
        txn.transfer_type = 'Wire'
    for txn in domestic_list:
        txn.transfer_type = 'Domestic'
 
    # --- Merge and sort by newest ---
    all_transfers = sorted(
        chain(wire_list, domestic_list),
        key=attrgetter('created_at'),
        reverse=True
    )
 
    # --- Stats counts (always from full unfiltered queryset) ---
    all_wire     = WireTransfer.objects.filter(user=request.user)
    all_domestic = DomesticTransfer.objects.filter(user=request.user)
    total_count    = all_wire.count()     + all_domestic.count()
    pending_count  = all_wire.filter(status='Pending').count()   + all_domestic.filter(status='Pending').count()
    completed_count= all_wire.filter(status='Completed').count() + all_domestic.filter(status='Completed').count()
    failed_count   = all_wire.filter(status='Failed').count()    + all_domestic.filter(status='Failed').count()
 
    # --- Paginate: 10 per page ---
    paginator    = Paginator(all_transfers, 10)
    page_number  = request.GET.get('page', 1)
    transactions = paginator.get_page(page_number)
 
    context = {
        'profile':          profile,
        'first_name':       request.user.first_name or request.user.username,
        'currency_display': profile.currency if profile else 'USD',
        'transactions':     transactions,
        'active_filter':    active_filter,
        'search_query':     search_query,
        'total_count':      total_count,
        'pending_count':    pending_count,
        'completed_count':  completed_count,
        'failed_count':     failed_count,
    }
    return render(request, 'app/transactions.html', context)


@login_required(login_url='app:login')
def loans(request):
    profile     = getattr(request.user, 'profile', None)
    first_name  = request.user.first_name or request.user.username
    user_loans  = LoanApplication.objects.filter(user=request.user)
 
    if request.method == 'POST':
        loan_type       = request.POST.get('loan_type', '').strip()
        amount          = request.POST.get('amount', '').strip()
        duration_months = request.POST.get('duration_months', '').strip()
        purpose         = request.POST.get('purpose', '').strip()
        monthly_income  = request.POST.get('monthly_income', '').strip()
 
        if not all([loan_type, amount, duration_months, purpose, monthly_income]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                LoanApplication.objects.create(
                    user=request.user,
                    loan_type=loan_type,
                    amount=Decimal(amount),
                    duration_months=int(duration_months),
                    purpose=purpose,
                    monthly_income=Decimal(monthly_income),
                    status='Pending',
                )
                messages.success(request, 'Loan application submitted successfully. We will review it shortly.')
                return redirect('bank:loans')
            except Exception:
                messages.error(request, 'Invalid amount or duration. Please check your inputs.')
 
    context = {
        'profile':    profile,
        'first_name': first_name,
        'user_loans': user_loans,
        'currency_display': profile.currency if profile else 'USD',
    }
    return render(request, 'app/dashloan.html', context)

import uuid

@login_required(login_url='app:signin')
def transfer_receipt(request, transfer_type, transfer_id):
    profile = getattr(request.user, 'profile', None)
 
    if transfer_type == 'wire':
        transfer = get_object_or_404(WireTransfer, id=transfer_id, user=request.user)
        transfer_type_label = 'Wire'
    else:
        transfer = get_object_or_404(DomesticTransfer, id=transfer_id, user=request.user)
        transfer_type_label = 'Domestic'
 
    # Generate a unique reference ID based on the transfer id
    reference_id = f"WU{transfer.id:06d}{str(uuid.uuid4()).replace('-','').upper()[:8]}"
 
    context = {
        'profile':          profile,
        'first_name':       request.user.first_name or request.user.username,
        'currency_display': profile.currency if profile else 'USD',
        'transfer':         transfer,
        'transfer_type':    transfer_type_label,
        'reference_id':     reference_id,
    }
    return render(request, 'app/transfer_receipt.html', context)



@login_required(login_url='bank:signin')
def verify_pin(request):
    profile = getattr(request.user, 'profile', None)

    if not profile or not profile.has_pin:
        return redirect('bank:set_pin')

    context = {
        'profile': profile,
        'first_name': request.user.first_name or request.user.username,
        'full_name': request.user.get_full_name() or request.user.username,
    }

    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()

        if profile.check_pin(pin):
            request.session['pin_verified'] = True
            next_url = request.session.pop('next_after_pin', None)
            return redirect(next_url or 'bank:dashboard')

        messages.error(request, 'Incorrect PIN. Please try again.')
        return render(request, 'bank/verify_pin.html', context)

    return render(request, 'bank/verify_pin.html', context)


from dateutil.relativedelta import relativedelta 

@login_required(login_url='app:login')
def deposits(request):
    profile        = getattr(request.user, 'profile', None)
    first_name     = request.user.first_name or request.user.username
    user_deposits  = Deposit.objects.filter(user=request.user)
 
    if request.method == 'POST':
        deposit_type    = request.POST.get('deposit_type', '').strip()
        amount          = request.POST.get('amount', '').strip()
        duration_months = request.POST.get('duration_months', '').strip()
        interest_rate   = request.POST.get('interest_rate', '5.00').strip()
 
        if not all([deposit_type, amount, duration_months]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                maturity = date.today() + relativedelta(months=int(duration_months))
                Deposit.objects.create(
                    user=request.user,
                    deposit_type=deposit_type,
                    amount=Decimal(amount),
                    duration_months=int(duration_months),
                    interest_rate=Decimal(interest_rate),
                    maturity_date=maturity,
                    status='Active',
                )
                messages.success(request, 'Deposit created successfully.')
                return redirect('bank:deposits')
            except Exception:
                messages.error(request, 'Invalid inputs. Please check your values.')
 
    context = {
        'profile':       profile,
        'first_name':    first_name,
        'user_deposits': user_deposits,
        'currency_display': profile.currency if profile else 'USD',
    }
    return render(request, 'app/deposits.html', context)



@login_required(login_url='app:login')
def profile_view(request):
    profile    = getattr(request.user, 'profile', None)
    first_name = request.user.first_name or request.user.username
    full_name  = request.user.get_full_name() or request.user.username
 
    context = {
        'profile':    profile,
        'first_name': first_name,
        'full_name':  full_name,
        'user':       request.user,
        'currency_display': profile.currency if profile else 'USD',
    }
    return render(request, 'app/profile.html', context)


@login_required(login_url='app:login')
def notifications(request):
    profile    = getattr(request.user, 'profile', None)
    first_name = request.user.first_name or request.user.username
    notifs     = Notification.objects.filter(user=request.user)
 
    # Mark all as read when page is opened
    notifs.filter(is_read=False).update(is_read=True)
 
    context = {
        'profile':       profile,
        'first_name':    first_name,
        'notifications': notifs,
    }
    return render(request, 'app/notifications.html', context)




@login_required(login_url='app:login')
def settings_view(request):
    profile    = getattr(request.user, 'profile', None)
    first_name = request.user.first_name or request.user.username
 
    if request.method == 'POST':
        action = request.POST.get('action')
 
        if action == 'change_pin':
            current_pin = request.POST.get('current_pin', '').strip()
            new_pin     = request.POST.get('new_pin', '').strip()
            confirm_pin = request.POST.get('confirm_pin', '').strip()
 
            if not profile.check_pin(current_pin):
                messages.error(request, 'Current PIN is incorrect.')
            elif not new_pin.isdigit() or len(new_pin) != 4:
                messages.error(request, 'New PIN must be exactly 4 digits.')
            elif new_pin != confirm_pin:
                messages.error(request, 'New PINs do not match.')
            else:
                profile.set_pin(new_pin)
                request.session.pop('pin_verified', None)
                messages.success(request, 'PIN changed successfully.')
            return redirect('bank:settings')
 
        if action == 'change_password':
            current_password = request.POST.get('current_password', '')
            new_password     = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
 
            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif len(new_password) < 6:
                messages.error(request, 'Password must be at least 6 characters.')
            elif new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password changed. Please sign in again.')
                return redirect('app:login')
            return redirect('app:settings')
 
    context = {
        'profile':    profile,
        'first_name': first_name,
    }
    return render(request, 'app/settings.html', context)
 
 
# ============================================================
# CONTEXT PROCESSOR - unread notification count for topbar badge
# Add this to a new file: bank/context_processors.py
# Then register it in settings.py TEMPLATES context_processors list:
# 'bank.context_processors.notification_count'
# ============================================================
def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications': count}
    return {'unread_notifications': 0} 






def personal(request):
    return render(request , "app/personal.html")

def cooperate(request):
    return render(request , "app/cooperate.html")

def insurance(request):
    return render(request,"app/insurance.html")

def mortgage(request):
    return render(request,"app/mortgage.html")
def terms(request):
    return render(request, "app/terms.html")

def contact(request):
    return render(request, "app/contact.html")
def card(request):
    return render(request, "app/credit.html")
def savings(request):
    return render(request, "app/savings.html")
def busloans(request):
    return render(request, "app/business.html")
def about(request):
    return render(request, 'app/about.html')

def logout_view(request):

    logout(request)

    return redirect("/login")