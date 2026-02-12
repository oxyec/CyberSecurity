from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Bulletin


def bulletin_list(request):
    query = request.GET.get('q')
    bulletins = Bulletin.objects.order_by('-published_at')

    if query:
        bulletins = bulletins.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, 'haberler/bulletin_list.html', {
        'bulletins': bulletins,
        'query': query,
    })


def bulletin_detail(request, pk):
    bulletin = get_object_or_404(Bulletin, pk=pk)
    return render(request, 'haberler/bulletin_detail.html', {
        'bulletin': bulletin,
    })