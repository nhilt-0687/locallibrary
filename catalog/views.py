from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from catalog.models import Book, Author, BookInstance
from catalog.constants import LoanStatus, DEFAULT_PAGINATION_SIZE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBookModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime


def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LoanStatus.AVAILABLE.value
    ).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    num_visits = num_visits + 1
    request.session['num_visits'] = num_visits
    request.session.modified = True

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = DEFAULT_PAGINATION_SIZE
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class AuthorDetailView(generic.DetailView):
    model = Author


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


@login_required
def my_borrowed_books(request):
    borrowed_books = BookInstance.objects.filter(
        borrower=request.user,
        status=LoanStatus.ON_LOAN.value
    )
    context = {
        'borrowed_books': borrowed_books,
        'LoanStatus': LoanStatus,
    }
    return render(request, 'catalog/my_borrowed_books.html', context=context)


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def mark_book_returned(request, bookinstance_id):
    bookinstance = get_object_or_404(BookInstance, id=bookinstance_id)
    if request.method == 'POST':
        bookinstance.status = LoanStatus.AVAILABLE.value
        bookinstance.borrower = None
        bookinstance.due_date = None
        bookinstance.save()
    return redirect('catalog:my_borrowed_books')


def team_name_view(request):
    if request.method == 'POST':
        team_name = request.POST.get('name_field')
        return render(
            request,
            'catalog/team_name_success.html',
            {'team_name': team_name}
        )
    return render(request, 'forms.html')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST, instance=book_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    else:
        initial_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(
            instance=book_instance,
            initial={'due_date': initial_date}
        )
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def all_borrowed_books(request):
    borrowed_books = BookInstance.objects.filter(
        status=LoanStatus.ON_LOAN.value
    )
    context = {
        'borrowed_books': borrowed_books,
        'LoanStatus': LoanStatus,
    }
    return render(request, 'catalog/all_borrowed_books.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'


class AuthorDelete(DeleteView):
    model = Author
    template_name = 'catalog/author_confirm_delete.html'
    success_url = reverse_lazy('catalog:authors')


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = DEFAULT_PAGINATION_SIZE
    template_name = 'catalog/author_list.html'
