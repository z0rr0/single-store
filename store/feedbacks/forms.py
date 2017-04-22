# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from feedbacks.models import Request


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ('product', 'name', 'phone', 'email', 'comment')
        widgets = {
            'product': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone number')}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Email address (optional)')}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': _('Additional comment'), 'rows': '3'}
            ),
        }
