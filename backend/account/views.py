from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import ExtractHour
from django.utils import timezone
import time

from account.models import LoginAttempt  # Bu model daha önce eklendiğini varsayıyoruz
from django.contrib.auth import get_user_model
from blog.models import Post, Comment

def main(request):
    return HttpResponse("Hello from main view!")

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            key = f'login_failures_{ip}'
            failures = cache.get(key, [])
            current_time = time.time()
            # Clean old failures (filter only recent ones)
            failures = [t for t in failures if current_time - t < 300]

            if len(failures) >= 5:
                messages.error(request, "Çok fazla başarısız giriş denemesi tespit edildi. Lütfen 5 dakika sonra tekrar deneyin.")
                return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ip = self.request.META.get('REMOTE_ADDR')
        cache.delete(f'login_failures_{ip}')  # Başarılı girişte sıfırla

        # Başarılı giriş denemesi veritabanına kaydedilir
        LoginAttempt.objects.create(
            username=form.cleaned_data.get('username'),
            ip_address=ip,
            successful=True,  # modelde 'successful' olarak tanımlı
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
def profile_view(request, username=None):
    User = get_user_model()
    if username is None:
        user_obj = request.user
    else:
        user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj)
    comments = Comment.objects.filter(author=user_obj)
    profile = getattr(user_obj, 'userprofile', None)
    return render(request, 'account/profile.html', {
        'profile_user': user_obj,
        'profile': profile,
        'posts': posts,
        'comments': comments,
    })

@login_required
def home(request):
    return render(request, 'account/home.html')
   

# Eklenen: davranış analizi view'i (mevcut yapıya eklendi, bozulmadan)
@login_required
def behavior_analysis_view(request):
    ip = request.META.get('REMOTE_ADDR')
    # Filter by username to show user's own activity, not global or shared IP activity
    username = request.user.username
    login_attempts = LoginAttempt.objects.filter(username=username).order_by('-timestamp')[:20]

    # Son 30 gün içindeki giriş saatlerinin dağılımı
    login_hours = (
        LoginAttempt.objects
        .filter(username=username, timestamp__gte=timezone.now() - timezone.timedelta(days=30))
        .annotate(hour=ExtractHour('timestamp'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Son 30 gündeki en çok kullanılan IP'ler (kullanıcı bazlı)
    top_ips = (
        LoginAttempt.objects
        .filter(username=username, timestamp__gte=timezone.now() - timezone.timedelta(days=30))
        .values('ip_address')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    current_hour = timezone.now().hour
    typical_hour = login_hours[0]['hour'] if login_hours else None
    unusual_time = typical_hour is not None and abs(current_hour - typical_hour) > 3

    context = {
        'attempts': login_attempts,
        'ip': ip,
        'login_hours': login_hours,
        'top_ips': top_ips,
        'current_hour': current_hour,
        'typical_hour': typical_hour,
        'unusual_time': unusual_time,
    }

    return render(request, 'account/behavior_analysis.html', context)
