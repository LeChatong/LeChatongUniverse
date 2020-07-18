from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from .models import movie_detail

class ConnexionForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        required=True,
        max_length=150,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'required':'true', 'placeholder': _('Username')},)
    )
    password = forms.CharField(
        label=_('Password'),
        required=True,
        max_length=150,
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'required':'true', 'placeholder': _('Password')},)
    )

class ConnectionError(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="error text-danger">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class MovieForm(forms.Form):
    LANGUAGE = (
        ('VF', 'VF'),
        ('VOSTFRJA', 'VOSTFR - JA'),
        ('VOSTFREN', 'VOSTFR - EN')
    )
    QUALITY = (
        ('HIGH', _('HIGH')),
        ('MEDIUM', _('MEDIUM')),
        ('LOW', _('LOW'))
    )
    link_download = forms.URLField(
        label=_('link_download'),
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-user', 'required': 'true', 'placeholder': _('link_download')}, )
    )
    language = forms.ChoiceField(
        choices=LANGUAGE,
        label= _('language'),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control form-control-user', 'required': 'true', 'placeholder': _('language')}, )
    )
    quality = forms.ChoiceField(
        choices=QUALITY,
        label=_('quality'),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control form-control-user', 'required': 'true', 'placeholder': _('quality')}, )
    )
