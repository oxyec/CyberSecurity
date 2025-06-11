from django.urls import path
from .views import blog_list, post_create

urlpatterns = [
    path('', blog_list, name='blog_list'),        
    path('new/', post_create, name='post_create') 
]
