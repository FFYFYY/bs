from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_view, name='search'),
    path('author/', views.author_view, name='author'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('book/<int:book_id>/', views.book_view, name='book'),
    path('like/<int:book_id>/', views.like_view, name='like')
]
