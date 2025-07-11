from django.shortcuts import render
<<<<<<< HEAD
from django.shortcuts import get_object_or_404
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=LoanStatus.AVAILABLE).count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
=======
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact=LoanStatus.AVAILABLE.value).count()
    num_authors = Author.objects.count()
>>>>>>> a2457d3 (Django Tutorial Part 5: Creating Our Home Page (#9))

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)
<<<<<<< HEAD

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
=======
>>>>>>> a2457d3 (Django Tutorial Part 5: Creating Our Home Page (#9))
