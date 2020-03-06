from django.db import models
from django.utils import translation
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

#model for the member on the application
class member(models.Model):
    first_name = models.CharField(verbose_name=_('first_name'), null=True, max_length=50)
    last_name = models.CharField(verbose_name=_('last_name'), null=True, max_length=50)
    username = models.CharField(verbose_name=_('username'), null=False, unique=True, max_length=100)
    password = models.CharField(verbose_name=_('password'), null=False, max_length=100)
    email = models.EmailField(verbose_name=_('email'), null=False, unique=True, max_length=150)
    created_at = models.DateTimeField(verbose_name=_('created_at'), default=timezone.now())
    last_connexion = models.DateTimeField(verbose_name=_('last_connexion'))
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)
    is_delete = models.BooleanField(verbose_name=_('is_delete'), default=False)
    is_modarator =  models.BooleanField(verbose_name=_('is_modarator'), default=False)
    #avatar =
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        ordering = ['username']
    def __str__(self):
        return self.username

#model for the canal telegram : the canal belong to a membe
class canal(models.Model):
    name = models.CharField(verbose_name=_('name_canal'), null=False, max_length=150)
    canal_link =  models.URLField(verbose_name=_('canal_link'), null=True, max_length=250)
    member = models.ForeignKey(member, on_delete=models.CASCADE)
    class Meta:
        verbose_name = _('canal')
        verbose_name_plural = _('canals')
        ordering = ['name']
    def __str__(self):
        return self.name
