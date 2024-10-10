import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import CustomUser


from django.shortcuts import render

def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is initially inactive until verified
            user.set_password(form.cleaned_data['password1'])  # Parolni hash qilish
            user.save()

            # Tasdiqlash kodi yaratish
            confirmation_code = random.randint(100000, 999999)
            request.session['confirmation_code'] = confirmation_code
            request.session['user_id'] = user.id

            # Tasdiqlash kodini email orqali yuborish
            send_mail(
                'Tasdiqlash kodingiz',
                f'Tasdiqlash kodi: {confirmation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('verify_email')  # Tasdiqlash sahifasiga o'tish
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        input_code = request.POST.get('confirmation_code')
        user_id = request.session.get('user_id')
        confirmation_code = request.session.get('confirmation_code')

        if str(input_code) == str(confirmation_code):
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True  # Activate user after verification
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('home')  # Asosiy sahifaga o'tish
        else:
            return render(request, 'verify_email.html', {'error': 'Tasdiqlash kodi noto‘g‘ri'})

    return render(request, 'verify_email.html')
