from django.urls import path
from . import views

urlpatterns = [
    path('', views.bulletin_list, name='bulletin_list'),
    path('<int:pk>/', views.bulletin_detail, name='bulletin_detail'), 
]
