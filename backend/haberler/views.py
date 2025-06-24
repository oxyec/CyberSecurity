from django.shortcuts import render
from django.db.models import Q
from .models import Bulletin

def bulletin_list(request):
    query = request.GET.get('q')  # Arama kutusundaki kelimeyi al
    bulletins = Bulletin.objects.order_by('-published_at')  # Yeni haberi en önce göster

    if query:
        bulletins = bulletins.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, 'haberler/bulletin_list.html', {
        'bulletins': bulletins,
        'query': query,  # HTML'de inputta göstermek için
    })
def bulletin_detail(request, pk):
    bulletin = Bulletin.objects.get(pk=pk)
    return render(request, 'haberler/bulletin_detail.html', {
        'bulletin': bulletin,
    })