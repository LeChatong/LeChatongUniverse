from django.db import models

# Create your models here.
class movie_detail(models.Model):
    id_movie = models.IntegerField()
    title_movie = models.CharField(max_length=250)
    link_telegram = models.URLField()
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

    voice_language = models.CharField(max_length=10, choices=LANGUAGE)
    quality_video = models.CharField(max_length=10, choices=QUALITY)
    quality_audio = models.CharField(max_length=10, choices=QUALITY)
    subtitle = models.CharField(max_length=3, choices=YES_OR_NO)
    subtitle_language = models.CharField(max_length=10, choices=LANGUAGE)
    class Meta:
        verbose_name    = 'movie_detail'
        ordering        = ['title_movie']
    def __str__(self):
        return self.title_movie

class tv_detail(models.Model):
    id_tv = models.IntegerField()
    nb_season = models.IntegerField(default=0)
    nb_episode = models.IntegerField(default=0)
    title_tv = models.CharField(max_length=250)
    link_telegram = models.URLField()
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

    voice_language = models.CharField(max_length=10, choices=LANGUAGE)
    quality_video = models.CharField(max_length=10, choices=QUALITY)
    quality_audio = models.CharField(max_length=10, choices=QUALITY)
    subtitle = models.CharField(max_length=3, choices=YES_OR_NO)
    subtitle_language = models.CharField(max_length=10, choices=LANGUAGE)
    class Meta:
        verbose_name    = 'tv_detail'
        ordering        = ['title_tv']
    def __str__(self):
        return self.title_tv
