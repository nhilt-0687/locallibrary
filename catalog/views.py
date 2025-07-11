from django.shortcuts import render
from .models import Book, Genre, BookInstance

def index(request):
    num_books = Book.objects.count()
    num_genres = Genre.objects.count()
    num_instances = BookInstance.objects.count()
    return render(request, 'catalog/index.html', {
        'num_books': num_books,
        'num_genres': num_genres,
        'num_instances': num_instances,
    })

def book_list(request):
    books = Book.objects.all().prefetch_related('genre', 'author')
    return render(request, 'catalog/book_list.html', {'books': books})
