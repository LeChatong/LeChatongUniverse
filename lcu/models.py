from django.db import models

# Create your models here.
#model for the member on the application
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class member(models.Model):
    first_name = models.CharField(verbose_name=_('first_name'), null=True, max_length=100)
    username = models.CharField(verbose_name=_('username'), null=False, unique=True, max_length=100)
    password = models.CharField(verbose_name=_('password'), null=False, max_length=100)
    email = models.EmailField(verbose_name=_('email'), null=False, unique=True, max_length=150)
    created_at = models.DateTimeField(verbose_name=_('created_at'), default=timezone.now)
    last_connexion = models.DateTimeField(verbose_name=_('last_connexion'), null=True)
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)
    is_delete = models.BooleanField(verbose_name=_('is_delete'), default=False)
    is_locked = models.BooleanField(verbose_name=_('is_locked'), default=False, null=True)
    is_modarator =  models.BooleanField(verbose_name=_('is_modarator'), default=False)
    avatar = models.ImageField(upload_to="avatar/")
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        ordering = ['username']
    def __str__(self):
        return self.username

class movie_detail(models.Model):
    id_movie = models.IntegerField()
    title_movie = models.CharField(verbose_name=_('titre'),max_length=250)
    link_download = models.URLField(verbose_name=_('lien_telechargement'))
    LANGUAGE = (
        ('FR', _('FRANÇAIS')),
        ('EN', _('ANGLAIS')),
        ('JP', _('JAPONAIS')),
        ('...', _('AUTRE')),
        ('N/A', _('AUCUN')),
    )
    QUALITY =  (
        ('GD', _('BONNE')),
        ('PASS', _('MOYENNE')),
        ('BAD', _('MAUVAISE')),
        ('N/A', _('AUCUN')),
    )
    YES_OR_NO = (
        ('Y', _('OUI')),
        ('N', _('NON')),
    )

    voice_language = models.CharField(verbose_name=_('langue'),max_length=10, choices=LANGUAGE)
    quality_video = models.CharField(verbose_name=_('qualite_video'),max_length=10, choices=QUALITY)
    quality_audio = models.CharField(verbose_name=_('qualite_audio'),max_length=10, choices=QUALITY)
    subtitle = models.CharField(verbose_name=_('est_soustitre'),max_length=3, choices=YES_OR_NO)
    subtitle_language = models.CharField(verbose_name=_('langue_du_soustitre'),max_length=10, choices=LANGUAGE)
    member = models.ForeignKey(member, on_delete=models.DO_NOTHING, null=True, default=1)
    created_at = models.DateTimeField(verbose_name=_('created_at'), null=True, default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), null=True, default=timezone.now)
    class Meta:
        verbose_name    = _('Film')
        verbose_name_plural = _('Films')
        ordering        = ['title_movie']
    def __str__(self):
        return self.title_movie

class tv_detail(models.Model):
    id_tv = models.IntegerField()
    nb_season = models.IntegerField(verbose_name=_('saison'),default=1)
    nb_episode = models.IntegerField(verbose_name=_('episode'),default=1)
    title_tv = models.CharField(verbose_name=_('titre'),max_length=250,)
    link_download = models.URLField(verbose_name=_('lien_telechargement'))
    LANGUAGE = (
        ('FR', _('FRANÇAIS')),
        ('EN', _('ANGLAIS')),
        ('JP', _('JAPONAIS')),
        ('...', _('AUTRE')),
        ('N/A', _('AUCUN')),
    )
    QUALITY = (
        ('GD', _('BONNE')),
        ('PASS', _('MOYENNE')),
        ('BAD', _('MAUVAISE')),
        ('N/A', _('AUCUN')),
    )
    YES_OR_NO = (
        ('Y', _('OUI')),
        ('N', _('NON')),
    )

    voice_language = models.CharField(verbose_name=_('langue'), max_length=10, choices=LANGUAGE)
    quality_video = models.CharField(verbose_name=_('qualite_video'),max_length=10, choices=QUALITY)
    quality_audio = models.CharField(verbose_name=_('qualite_audio'),max_length=10, choices=QUALITY)
    subtitle = models.CharField(verbose_name=_('est_soustitre'),max_length=3, choices=YES_OR_NO)
    subtitle_language = models.CharField(verbose_name=_('langue_du_soustitre'),max_length=10, choices=LANGUAGE)
    member = models.ForeignKey(member, on_delete=models.DO_NOTHING, null=True, default=1)
    created_at = models.DateTimeField(verbose_name=_('created_at'), null=True, default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), null=True, default=timezone.now)
    class Meta:
        verbose_name    = _('serie_anime')
        verbose_name_plural = _('series_animes')
        ordering        = ['title_tv']
    def __str__(self):
        return self.title_tv

class comment(models.Model):
    name_sender = models.CharField(verbose_name=_('name_sender'),max_length=150, null=False)
    message = models.CharField(verbose_name=_('message'), max_length=250, null=False)
    email_sender = models.EmailField(verbose_name=_('email_sender'), max_length=150, null=True)
    id_movie = models.IntegerField(null=True)
    id_tv = models.IntegerField(null=True)
    is_reply = models.BooleanField(verbose_name=_('is_reply'), default=False)
    is_delete = models.BooleanField(verbose_name=_('is_delete'), default=False)
    is_locked = models.BooleanField(verbose_name=_('is_locked'), default=False)
    comment_parent_id = models.IntegerField(null=True)
    member = models.ForeignKey(member, on_delete=models.DO_NOTHING, null=True, default=1)
    created_at = models.DateTimeField(verbose_name=_('created_at'), null=True, default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), null=True, default=timezone.now)
    class Meta:
        verbose_name    = _('comment')
        verbose_name_plural = _('comments')
        ordering        = ['name_sender']
    def __str__(self):
        return self.name_sender