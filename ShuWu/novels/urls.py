from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('author/', views.author_view, name='author'),
    path('book/<int:book_id>/', views.book_view, name='book'),
    path('like/<int:book_id>/', views.like_view, name='like'),
    path('support/<int:url_id>', views.support_view),
    path('against/<int:url_id>', views.against_view),
    path('shareurls/', views.share_view),
    path('manage/manage-share-urls/', views.msu_view, name='msu'),
    path('addurl/<int:url_id>', views.addurl_view),
    path('deleteurl/<int:url_id>', views.deleteurl_view)
]
