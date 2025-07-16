from django.shortcuts import render, get_object_or_404
from django.views import generic
from catalog.models import Book, Author, BookInstance
from catalog.constants import LoanStatus, DEFAULT_PAGINATION_SIZE


def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LoanStatus.AVAILABLE
    ).count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = DEFAULT_PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_instances'] = \
            self.object.bookinstance_set.select_related().all()
        return context


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    book_instances = book.bookinstance_set.select_related().all()

    context = {
        'book': book,
        'book_instances': book_instances,
    }
    return render(
        request,
        'catalog/book_detail.html',
        context=context
    )
