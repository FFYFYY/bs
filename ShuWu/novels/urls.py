from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search', views.search_view, name='search'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('novel/<int>', views.novel_view, name='novel')
]
