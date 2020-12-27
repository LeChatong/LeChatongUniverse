from django import forms

from django.forms.utils import ErrorList

from django.utils.translation import ugettext_lazy as _

class InitPasswordForm(forms.Form):
    password = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    confirm_password = forms.CharField(label=_("Password Confirm"), widget=forms.PasswordInput)

    def clean_confirm_password(self):
        cleaned_data = super(InitPasswordForm, self).clean()
        if cleaned_data.get('confirm_password') != cleaned_data.get('password'):
            self.add_error("confirm_password",
                           _('Mot de passe non conforme')
                           )

        return cleaned_data

class InitPasswordErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])