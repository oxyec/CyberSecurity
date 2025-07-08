from django.urls import path
from .views import CustomLoginView, behavior_analysis_view
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('behavior/', behavior_analysis_view, name='behavior-analysis'),  # ← Burayı ekledik
    path('<str:username>/', views.profile_view, name='user_profile'),
]
