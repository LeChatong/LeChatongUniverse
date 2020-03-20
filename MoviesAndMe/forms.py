from django import  forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from lcu.models import comment

class CommentForm(ModelForm):
    name_sender = forms.CharField(
        label=_('Votre nom'),
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control required', 'required':'true', 'placeholder': _('Votre nom')},)
    )
    email_sender = forms.EmailField(
        label=_('Votre Email'),
        required=False,
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label=_('Votre Commentaire'),
        required=True,
        max_length=250,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Message')})
    )
    save_in_browser = forms.BooleanField(
        label=_('save_name_and_mail_in_broswer_for_next_comment'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    )
    comment_parent_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    member = forms.HiddenInput
    class Meta:
        model = comment
        fields = ['name_sender', 'email_sender', 'message', 'id_movie', 'id_tv', 'member', 'created_at', 'updated_at', 'save_in_browser', 'comment_parent_id']