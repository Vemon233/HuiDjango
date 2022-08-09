from django.urls import path
from EPaCMonitor import views

app_name = 'EPaCMonitor'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('undiagnosed/', views.undiagnosed, name='undiagnosed'),
    path('list_less/', views.list_less, name='list_less'),
    path('list_common/', views.list_common, name='list_common'),
    path('list_frequent/', views.list_frequent, name='list_frequent'),
    path('search/', views.search, name='search'),
]
