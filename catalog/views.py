from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus

def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=LoanStatus.AVAILABLE).count()
    num_authors = Author.objects.count() 

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})
