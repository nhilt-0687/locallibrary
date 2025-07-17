from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Book, Author, BookInstance
from catalog.constants import LoanStatus, DEFAULT_PAGINATION_SIZE
from django.utils import timezone
import datetime
import uuid


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.author = Author.objects.create(first_name='John', last_name='Doe')
        self.book = Book.objects.create(title='Test Book', author=self.author)
        self.book_instance = BookInstance.objects.create(
            id=uuid.UUID('123e4567-e89b-12d3-a456-426614174000'),
            book=self.book,
            status=LoanStatus.ON_LOAN.value,
            borrower=self.user,
            due_date=timezone.localtime().date() + datetime.timedelta(days=5)
        )

    def test_index_view(self):
        response = self.client.get(reverse('catalog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tổng số sách')
        self.assertContains(response, '1 sách')
        self.assertContains(response, 'Bạn đã ghé thăm trang này 1 lần')

    def test_book_detail_view(self):
        response = self.client.get(
            reverse(
                'catalog:book_detail',
                kwargs={'primary_key': self.book.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_my_borrowed_books_login_required(self):
        response = self.client.get(reverse('catalog:my_borrowed_books'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('catalog:my_borrowed_books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertContains(
            response,
            'Hạn trả: Ngày 22 tháng 7 năm 2025'
        )
        self.assertEqual(response.context['borrowed_books'].count(), 1)
        self.assertEqual(
            response.context['borrowed_books'][0].id,
            self.book_instance.id
        )

    def test_renew_book_librarian_valid(self):
        self.client.login(username='testuser', password='12345')
        url = reverse(
            'catalog:renew_book_librarian',
            kwargs={'pk': self.book_instance.id}
        )
        valid_date = timezone.localtime().date() + datetime.timedelta(weeks=3)
        response = self.client.post(url, {'due_date': valid_date})
        self.assertEqual(response.status_code, 302)
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.due_date, valid_date)

    def test_renew_book_librarian_invalid_date(self):
        self.client.login(username='testuser', password='12345')
        url = reverse(
            'catalog:renew_book_librarian',
            kwargs={'pk': self.book_instance.id}
        )
        invalid_date = timezone.localtime().date() - datetime.timedelta(days=1)
        response = self.client.post(url, {'due_date': invalid_date})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Ngày không hợp lệ - không được chọn ngày trong quá khứ'
        )

    def test_mark_book_returned_success(self):
        self.client.login(username='testuser', password='12345')
        url = reverse(
            'catalog:mark_book_returned',
            kwargs={'bookinstance_id': str(self.book_instance.id)}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.status, LoanStatus.AVAILABLE.value)
        self.assertIsNone(self.book_instance.borrower)

    def test_mark_book_returned_permission_denied(self):
        another_user = User.objects.create_user(
            username='anotheruser',
            password='12345'
        )
        self.client.login(username='anotheruser', password='12345')
        url = reverse(
            'catalog:mark_book_returned',
            kwargs={'bookinstance_id': str(self.book_instance.id)}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_team_name_view_post(self):
        response = self.client.post(
            reverse('catalog:team_name'),
            {'name_field': 'Team A'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team A')

    def test_all_borrowed_books_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('catalog:all-borrowed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.book_instance.id))

    def test_author_create_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('catalog:author-create')
        response = self.client.post(url, {
            'first_name': 'New',
            'last_name': 'Author',
            'date_of_birth': '1990-01-01',
            'date_of_death': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.filter(last_name='Author').exists())

    def test_book_list_view_pagination(self):
        for i in range(DEFAULT_PAGINATION_SIZE + 1):
            Book.objects.create(title=f'Book {i}', author=self.author)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('catalog:books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(
            len(response.context['book_list']),
            DEFAULT_PAGINATION_SIZE
        )
