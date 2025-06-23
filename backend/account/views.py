from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Count
import time

from account.models import LoginAttempt  # Bu model daha önce eklendiğini varsayıyoruz

def main(request):
    return HttpResponse("Hello from main view!")

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        ip = self.request.META.get('REMOTE_ADDR')
        cache.delete(f'login_failures_{ip}')  # Başarılı girişte sıfırla

        # Başarılı giriş denemesi veritabanına kaydedilir
        LoginAttempt.objects.create(
            username=form.cleaned_data.get('username'),
            ip_address=ip,
            successful=True,  # düzeltme: modelde 'was_successful' değil 'successful' vardı
            timestamp=now()
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        ip = self.request.META.get('REMOTE_ADDR')
        username = form.data.get('username', 'unknown')

        # cache tarafı
        key = f'login_failures_{ip}'
        failures = cache.get(key, [])
        current_time = time.time()
        failures = [t for t in failures if current_time - t < 300]  # Son 5 dakikadakiler
        failures.append(current_time)
        cache.set(key, failures, timeout=300)

        # veritabanına başarısız giriş kaydı
        LoginAttempt.objects.create(
            username=username,
            ip_address=ip,
            successful=False,
            timestamp=now()
        )

        if len(failures) >= 5:
            messages.error(self.request, "Çok fazla başarısız giriş denemesi tespit edildi. Lütfen 5 dakika sonra tekrar deneyin.")
            return redirect('login')

        messages.error(self.request, "Kullanıcı adı veya şifre yanlış.")
        return super().form_invalid(form)

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})

# Eklenmesi gereken: davranış analizi view'i
@login_required
def behavior_analysis_view(request):
    ip = request.META.get('REMOTE_ADDR')
    login_attempts = LoginAttempt.objects.filter(ip_address=ip).order_by('-timestamp')[:20]

    return render(request, 'account/behavior_analysis.html', {
        'attempts': login_attempts,
        'ip': ip,
    })
