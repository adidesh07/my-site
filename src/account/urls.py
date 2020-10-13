from django.urls import path
from .views import account_view, my_blogs_view

app_name = 'account'

urlpatterns = [
    path('details/', account_view, name='details'),
    path('blogs/', my_blogs_view, name='my_blogs'),
]