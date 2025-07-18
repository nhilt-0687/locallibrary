from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Author, Book, BookInstance, Genre, Language
from django.utils import timezone
import datetime
import uuid


class ModelTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Fiction')
        self.language = Language.objects.create(name='English')
        self.author = Author.objects.create(
            first_name='Jane',
            last_name='Austen',
            date_of_birth=timezone.make_aware(datetime.datetime(1775, 12, 16)),
            date_of_death=timezone.make_aware(datetime.datetime(1817, 7, 18))
        )
        self.book = Book.objects.create(
            title='Pride and Prejudice',
            author=self.author,
            summary='A novel by Jane Austen',
            isbn='1234567890123',
            language=self.language
        )
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        content_type = ContentType.objects.get_for_model(BookInstance)
        permission = Permission.objects.get(
            codename='can_mark_returned',
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

        self.book_instance = BookInstance.objects.create(
            id=uuid.uuid4(),
            book=self.book,
            status='o',
            borrower=self.user,
            due_date=timezone.localtime().date() + datetime.timedelta(days=5)
        )

    def test_author_string_representation(self):
        self.assertEqual(str(self.author), 'Austen, Jane')

    def test_book_string_representation(self):
        self.assertEqual(str(self.book), 'Pride and Prejudice')

    def test_bookinstance_string_representation(self):
        self.assertEqual(
            str(self.book_instance),
            f'{self.book_instance.id} (Pride and Prejudice)'
        )

    def test_author_get_absolute_url(self):
        expected_url = f'/vi/catalog/author/{self.author.id}/'
        self.assertEqual(self.author.get_absolute_url(), expected_url)

    def test_book_get_absolute_url(self):
        expected_url = f'/vi/catalog/book/{self.book.id}/'
        self.assertEqual(self.book.get_absolute_url(), expected_url)

    def test_bookinstance_is_overdue(self):
        self.book_instance.due_date = timezone.localtime().date() - datetime.timedelta(days=1)
        self.book_instance.save()
        self.assertTrue(self.book_instance.is_overdue)

    def test_author_ordering(self):
        author2 = Author.objects.create(first_name='Zoe', last_name='Smith')
        authors = Author.objects.all()
        self.assertEqual(list(authors), [self.author, author2])

    def test_book_genre_relationship(self):
        genre2 = Genre.objects.create(name='Romance')
        self.book.genre.add(genre2)
        self.assertEqual(self.book.genre.count(), 2)

    def test_bookinstance_unique_id(self):
        new_instance = BookInstance.objects.create(
            id=uuid.uuid4(),
            book=self.book,
            status='a'
        )
        self.assertNotEqual(self.book_instance.id, new_instance.id)

    def test_bookinstance_default_status(self):
        new_instance = BookInstance.objects.create(book=self.book)
        self.assertEqual(new_instance.status, 'm')

    def test_bookinstance_permissions(self):
        self.assertTrue(self.user.has_perm('catalog.can_mark_returned'))

    def test_language_string_representation(self):
        self.assertEqual(str(self.language), 'English')
