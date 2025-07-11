from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
=======
    # path('books/', views.book_list, name='book_list'),
    # path('authors/', views.author_list, name='author_list'),
    # path('book/<int:pk>/', views.book_detail, name='book_detail'),
>>>>>>> a2457d3 (Django Tutorial Part 5: Creating Our Home Page (#9))
    # path('author/<int:pk>/', views.author_detail, name='author_detail'),
]
