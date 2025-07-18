import datetime
from django import forms
from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookModelForm
from catalog.models import BookInstance


class RenewBookFormTest(TestCase):
    def setUp(self):
        self.book_instance = BookInstance.objects.create(
            id='123e4567-e89b-12d3-a456-426614174000',
            status='o',
            due_date=timezone.localtime().date() + datetime.timedelta(weeks=2)
        )

    def test_renew_form_date_field_label(self):
        form = RenewBookModelForm()
        self.assertEqual(form.fields['due_date'].label, 'Ngày gia hạn')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookModelForm()
        self.assertEqual(
            form.fields['due_date'].help_text,
            'Nhập ngày trong khoảng từ hôm nay đến 4 tuần (mặc định 3 tuần).'
        )

    def test_renew_form_date_in_past(self):
        date = timezone.localtime().date() - datetime.timedelta(days=1)
        form = RenewBookModelForm(
            data={'due_date': date},
            instance=self.book_instance
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['due_date'],
            ['Ngày không hợp lệ - không được chọn ngày trong quá khứ']
        )

    def test_renew_form_date_too_far_in_future(self):
        date = timezone.localtime().date() + \
            datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookModelForm(
            data={'due_date': date},
            instance=self.book_instance
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['due_date'],
            ['Ngày không hợp lệ - không được chọn ngày quá 4 tuần']
        )

    def test_renew_form_date_today(self):
        date = timezone.localtime().date()
        form = RenewBookModelForm(
            data={'due_date': date},
            instance=self.book_instance
        )
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime().date() + datetime.timedelta(weeks=4)
        form = RenewBookModelForm(
            data={'due_date': date},
            instance=self.book_instance
        )
        self.assertTrue(form.is_valid())

    def test_renew_form_date_exactly_four_weeks_with_instance(self):
        date = timezone.localtime().date() + datetime.timedelta(weeks=4)
        form = RenewBookModelForm(
            data={'due_date': date},
            instance=self.book_instance
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['due_date'], date)

    def test_renew_form_empty_data(self):
        form = RenewBookModelForm(data={}, instance=self.book_instance)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_renew_form_invalid_date_format(self):
        form = RenewBookModelForm(
            data={'due_date': 'invalid-date'},
            instance=self.book_instance
        )
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_renew_form_widget_type_and_attrs(self):
        form = RenewBookModelForm()
        widget = form.fields['due_date'].widget
        self.assertIsInstance(widget, forms.widgets.DateInput)
        html_output = widget.render('due_date', None)
        self.assertIn('type="text"', html_output)

    def test_renew_form_internationalization(self):
        with self.settings(LANGUAGE_CODE='vi'):
            form = RenewBookModelForm()
            expected_help_text = (
                'Nhập ngày trong khoảng từ hôm nay đến 4 tuần (mặc định 3 tuần).'
            )
            self.assertEqual(
                form.fields['due_date'].help_text,
                expected_help_text
            )

    def test_renew_form_preserve_existing_due_date(self):
        original_due_date = self.book_instance.due_date
        form = RenewBookModelForm(instance=self.book_instance)
        self.assertEqual(form.initial['due_date'], original_due_date)
