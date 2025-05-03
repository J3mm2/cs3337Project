from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>/', views.book_delete, name='book_delete'),
    path('about_us/', views.about_us, name='about_us'),
    path('toggle_favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('search/', views.search_books, name='search_books'),
]