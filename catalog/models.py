from django.db import models
from django.utils.translation import gettext_lazy as _
from .constants import MAX_LENGTH_NAME, MAX_LENGTH_AUTHOR_NAME, MAX_LENGTH_ISBN, MAX_LENGTH_SUMMARY, MAX_LENGTH_UNIQUE_ID
from django.urls import reverse
import uuid
class Genre(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME, help_text=_("Enter the genre (e.g. Science Fiction)"))
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME, help_text=_("Enter the language (e.g. English)"))
    
    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH_AUTHOR_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_AUTHOR_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(_("died"), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

class Book(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_NAME)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=MAX_LENGTH_SUMMARY, help_text=_("Enter a brief description of the book"))
    isbn = models.CharField(_("ISBN"), max_length=MAX_LENGTH_ISBN, help_text=_("13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>"))
    genre = models.ManyToManyField(Genre, help_text=_("Select a genre for this book"))
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(null=True, blank=True)
    imprint = models.CharField(max_length=200, blank=True, null=True, help_text="Enter the publisher imprint")
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('on_loan', 'On Loan'),
        ('reserved', 'Reserved'),
    ], default='available')

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    