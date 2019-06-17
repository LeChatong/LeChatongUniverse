from django.db import models

# Create your models here.
class movie_detail(models.Model):
    id_movie = models.IntegerField()
    title_movie = models.CharField(verbose_name='Titre',max_length=250)
    link_telegram = models.URLField(verbose_name='Lien Télégram')
    LANGUAGE = (
        ('FRANÇAIS', 'FRANÇAIS'),
        ('ANGLAIS', 'ANGLAIS'),
        ('JAPONAIS', 'JAPONAIS'),
        ('AUCUN', 'AUCUN'),
    )
    QUALITY =  (
        ('BONNE', 'BONNE'),
        ('MOYENNE', 'MOYENNE'),
        ('MAUVAISE', 'MAUVAISE'),
        ('AUCUN', 'AUCUN'),
    )
    YES_OR_NO = (
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    )

    voice_language = models.CharField(verbose_name='Langue',max_length=10, choices=LANGUAGE)
    quality_video = models.CharField(verbose_name='Qualité Vidéo',max_length=10, choices=QUALITY)
    quality_audio = models.CharField(verbose_name='Qualité Audio',max_length=10, choices=QUALITY)
    subtitle = models.CharField(verbose_name='Soutitré ?',max_length=3, choices=YES_OR_NO)
    subtitle_language = models.CharField(verbose_name='Langue du Sous-titre',max_length=10, choices=LANGUAGE)
    class Meta:
        verbose_name    = 'Film'
        verbose_name_plural = 'Films'
        ordering        = ['title_movie']
    def __str__(self):
        return self.title_movie

class tv_detail(models.Model):
    id_tv = models.IntegerField()
    nb_season = models.IntegerField(verbose_name='Saison',default=0)
    nb_episode = models.IntegerField(verbose_name='Episode',default=0)
    title_tv = models.CharField(verbose_name='Titre',max_length=250)
    link_telegram = models.URLField(verbose_name='Lien Télégram')
    LANGUAGE = (
        ('FRANÇAIS', 'FRANÇAIS'),
        ('ANGLAIS', 'ANGLAIS'),
        ('JAPONAIS', 'JAPONAIS'),
        ('AUCUN', 'AUCUN'),
    )
    QUALITY =  (
        ('BONNE', 'BONNE'),
        ('MOYENNE', 'MOYENNE'),
        ('MAUVAISE', 'MAUVAISE'),
        ('AUCUN', 'AUCUN'),
    )
    YES_OR_NO = (
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    )

    voice_language = models.CharField(verbose_name='Langue', max_length=10, choices=LANGUAGE)
    quality_video = models.CharField(verbose_name='Qualité Vidéo',max_length=10, choices=QUALITY)
    quality_audio = models.CharField(verbose_name='Qualité Audio',max_length=10, choices=QUALITY)
    subtitle = models.CharField(verbose_name='Soutitré ?',max_length=3, choices=YES_OR_NO)
    subtitle_language = models.CharField(verbose_name='Langue du Sous-titre',max_length=10, choices=LANGUAGE)
    class Meta:
        verbose_name    = 'Série/Animé'
        verbose_name_plural = 'Séries/Animés'
        ordering        = ['title_tv']
    def __str__(self):
        return self.title_tv
