from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'account/login.html', {
            'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'
        })

    return render(request, 'account/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'account/register.html', {
                'error': 'اسم المستخدم موجود مسبقاً'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'account/register.html')


@login_required
def profile_view(request):
    user = request.user

    # ensure a profile exists
    profile, created = getattr(user, 'profile', (None, True)) if False else (None, None)
    try:
        profile = user.profile
    except Exception:
        from .models import UserProfile
        profile = UserProfile.objects.create(user=user, full_name=user.username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح')
            return redirect('profile')
        else:
            messages.error(request, 'هناك أخطاء في النموذج. أصلحها ثم أعد المحاولة.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'account/profile.html', {'form': form})
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'account/dashboard.html')
   

def logout_view(request):
    logout(request)
    return redirect('home')