from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('mybooks/', views.my_borrowed_books, name='my_borrowed_books'),
    path(
        'bookinstance/<uuid:bookinstance_id>/return/',
        views.mark_book_returned,
        name='mark_book_returned'
    ),
]
