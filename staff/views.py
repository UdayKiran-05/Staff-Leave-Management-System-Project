from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Leave
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
def home(request):
    return render(request, 'home.html')
# Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Check if username exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })
        #  Create user
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')
# Login
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
    return render(request, 'login.html')
# Logout
def user_logout(request):
    logout(request)
    return redirect('home')   # redirect to home page
# User Dashboard
def dashboard(request):
    return render(request, 'dashboard.html')
# Apply Leave
from datetime import datetime
def apply_leave(request):
    leaves = Leave.objects.filter(user=request.user)
    total_days = 20
    used_days = sum([l.approved_days for l in leaves])
    balance = total_days - used_days
    if request.method == 'POST':
        start = datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        end = datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        # Calculate requested days
        requested_days = (end - start).days + 1
        # ADD THIS CHECK HERE
        if requested_days > balance:
            messages.error(request, "Not enough leave balance!")
            return redirect('apply_leave')
        # If valid, save
        Leave.objects.create(
            user=request.user,
            leave_type=request.POST['leave_type'],
            start_date=start,
            end_date=end,
            reason=request.POST['reason']
        )
        messages.success(request, "Leave applied successfully")
        return redirect('my_leaves')
    return render(request, 'apply_leave.html')
# View Leaves
def my_leaves(request):
    leaves = Leave.objects.filter(user=request.user)
    total_days = 20
    used_days = sum([leave.approved_days for leave in leaves])
    balance = total_days - used_days
    #  NEW COUNTS
    approved_count = leaves.filter(status="Approved").count()
    pending_count = leaves.filter(status="Pending").count()
    rejected_count = leaves.filter(status="Rejected").count()
    return render(request, 'my_leaves.html', {
        'leaves': leaves,
        'balance': balance,
        'used_days': used_days,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count
    })
# Edit Leaves
from datetime import datetime
def edit_leave(request, id):
    leave = Leave.objects.get(id=id)
    #  Restrict if not pending
    if leave.status != "Pending":
        return redirect('my_leaves')
    if request.method == 'POST':
        leave.leave_type = request.POST['leave_type']
        leave.start_date = datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        leave.end_date = datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        leave.reason = request.POST['reason']
        leave.save()
        return redirect('my_leaves')
    return render(request, 'edit_leave.html', {'leave': leave})
def admin_home(request):
    return render(request, 'admin_home.html')
# Admin Dashboard
def admin_dashboard(request):
    status_filter = request.GET.get('status')
    if status_filter:
        leaves = Leave.objects.filter(status=status_filter)
    else:
        leaves = Leave.objects.all()
    search = request.GET.get('search')
    if search:
        leaves = Leave.objects.filter(user__username__icontains=search)
    return render(request, 'admin_dashboard.html', {
        'leaves': leaves
    })
# Approve
def approve_leave(request, id):
    leave = Leave.objects.get(id=id)
    if leave.status != "Pending":
        return redirect('admin_dashboard')
    # Calculate balance (excluding current leave)
    leaves = Leave.objects.filter(user=leave.user).exclude(id=leave.id)
    total_days = 20
    used_days = sum([l.approved_days for l in leaves])
    balance = total_days - used_days
    if request.method == 'POST':
        approved_days = int(request.POST['approved_days'])
        #  Validation
        if approved_days > balance:
            messages.error(request, "Not enough balance!")
            return redirect('admin_dashboard')
        if approved_days > leave.days:
            messages.error(request, "Cannot approve more than requested days!")
            return redirect('admin_dashboard')
        #  Save approval
        leave.approved_days = approved_days
        leave.status = "Approved"
        leave.save()
        return redirect('admin_dashboard')
    return render(request, 'approve_leave.html', {
        'leave': leave,
        'balance': balance
    })
# Reject
def reject_leave(request, id):
    leave = Leave.objects.get(id=id)
    if leave.status != "Pending":
        return redirect('admin_dashboard')
    leave.status = "Rejected"
    leave.save()
    return redirect('admin_dashboard')
# Delete
def delete_leave(request, id):
    leave = Leave.objects.get(id=id)
    # Allow delete only if pending
    if leave.status == "Pending":
        leave.delete()
    return redirect('my_leaves')
# Manage Users
def manage_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'manage_users.html', {
        'users': users
    })


# Edit User
def edit_user(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()

        return redirect('manage_users')

    return render(request, 'edit_user.html', {
        'user': user
    })


# Delete User
def delete_user(request, id):
    user = User.objects.get(id=id)

    if not user.is_superuser:
        user.delete()

    return redirect('manage_users')


# Reset Password
def reset_password(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        new_password = request.POST['password']

        user.set_password(new_password)
        user.save()

        return redirect('manage_users')

    return render(request, 'reset_password.html', {
        'user': user
    })