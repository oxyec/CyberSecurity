from django.urls import path
from .views import CustomLoginView, behavior_analysis_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('behavior/', behavior_analysis_view, name='behavior-analysis'),  # ← Burayı ekledik
]
