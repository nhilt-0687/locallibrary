from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import BookInstance
import datetime


class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_date']
        labels = {'due_date': _('Renewal date')}
        help_texts = {
            'due_date': _(
                'Enter a date between today and 4 weeks '
                '(default 3 weeks).'
            )
        }

    def clean_due_date(self):
        data = self.cleaned_data['due_date']
        if data is None:
            raise ValidationError(_('Invalid date - please enter a renewal date.'))
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in the past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks '
                  'ahead')
            )
        return data
