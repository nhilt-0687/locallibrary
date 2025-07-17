from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path(
        'book/<int:primary_key>/',
        views.book_detail_view,
        name='book_detail'
    ),
    path('mybooks/', views.my_borrowed_books, name='my_borrowed_books'),
    path(
        'bookinstance/<uuid:bookinstance_id>/return/',
        views.mark_book_returned,
        name='mark_book_returned'
    ),
    path('team_name_url/', views.team_name_view, name='team_name'),
    path(
        'book/<uuid:pk>/renew/',
        views.renew_book_librarian,
        name='renew_book_librarian'
    ),
    path('all-borrowed/', views.all_borrowed_books, name='all-borrowed'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path(
        'author/<int:pk>/update/',
        views.AuthorUpdate.as_view(),
        name='author-update'
    ),
    path(
        'author/<int:pk>/delete/',
        views.AuthorDelete.as_view(),
        name='author-delete'
    ),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path(
        'author/<int:pk>/',
        views.AuthorDetailView.as_view(),
        name='author-detail'
    ),
]
