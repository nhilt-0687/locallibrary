from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Author, Book, Genre, Language, BookInstance
from .constants import DEFAULT_IMPRINT


class BookInstanceInline(admin.TabularInline):
    """Inline editing for BookInstances related to a Book."""
    model = BookInstance
    extra = 0
    fields = ('id', 'imprint', 'due_date', 'status', 'borrower')
    readonly_fields = ('id',)


class BookInline(admin.TabularInline):
    """Inline editing for Books related to an Author."""
    model = Book
    extra = 0
    fields = ('title', 'language', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death')
    search_fields = ['last_name', 'first_name']
    list_filter = ('date_of_birth', 'date_of_death')
    ordering = ['last_name', 'first_name']
    inlines = [BookInline]

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name')
        }),
        ('Dates', {
            'fields': ('date_of_birth', 'date_of_death'),
            'description':
                'Use calendar to select dates.'
        }),
    )


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    list_filter = ('language', 'genre', 'author')
    search_fields = ('title', 'author__last_name', 'isbn')
    prefetch_related = ('genre',)
    inlines = [BookInstanceInline]

    def display_genre(self, obj):
        """Display up to 3 genres for the book."""
        return ', '.join([genre.name for genre in obj.genre.all()[:3]])
    display_genre.short_description = 'Genre'

    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'language')
        }),
        ('Details', {
            'fields': ('summary', 'isbn', 'genre'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('genre',)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status', 'borrower', 'due_date')
    list_filter = ('status', 'due_date', 'borrower')
    search_fields = ('id', 'book__title', 'borrower__username')
    date_hierarchy = 'due_date'
    list_editable = ('status',)
    readonly_fields = ('id',)

    fieldsets = (
        ('Instance Information', {
            'fields': ('id', 'book', 'status')
        }),
        ('Loan Information', {
            'fields': ('borrower', 'due_date'),
            'description':
                'Set borrower and due date for loaned books.'
        }),
        ('Additional Info', {
            'fields': ('imprint',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set default imprint and due_date if not provided."""
        if not obj.imprint:
            obj.imprint = DEFAULT_IMPRINT
        if not obj.id and not obj.due_date:
            obj.due_date = timezone.now() + timedelta(days=30)
        super().save_model(request, obj, form, change)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Genre)
admin.site.register(Language)
