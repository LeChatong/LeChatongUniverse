# Generated by Django 2.1.1 on 2020-02-14 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoviesAndMe', '0004_auto_20190614_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie_detail',
            options={'ordering': ['title_movie'], 'verbose_name': 'Film', 'verbose_name_plural': 'Films'},
        ),
        migrations.AlterModelOptions(
            name='tv_detail',
            options={'ordering': ['title_tv'], 'verbose_name': 'Série/Animé', 'verbose_name_plural': 'Séries/Animés'},
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='link_telegram',
            field=models.URLField(verbose_name='Lien Télégram'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='quality_audio',
            field=models.CharField(choices=[('BONNE', 'BONNE'), ('MOYENNE', 'MOYENNE'), ('MAUVAISE', 'MAUVAISE'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Qualité Audio'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='quality_video',
            field=models.CharField(choices=[('BONNE', 'BONNE'), ('MOYENNE', 'MOYENNE'), ('MAUVAISE', 'MAUVAISE'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Qualité Vidéo'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='subtitle',
            field=models.CharField(choices=[('OUI', 'OUI'), ('NON', 'NON')], max_length=3, verbose_name='Soutitré ?'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='subtitle_language',
            field=models.CharField(choices=[('FRANÇAIS', 'FRANÇAIS'), ('ANGLAIS', 'ANGLAIS'), ('JAPONAIS', 'JAPONAIS'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Langue du Sous-titre'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='title_movie',
            field=models.CharField(max_length=250, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='voice_language',
            field=models.CharField(choices=[('FRANÇAIS', 'FRANÇAIS'), ('ANGLAIS', 'ANGLAIS'), ('JAPONAIS', 'JAPONAIS'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Langue'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='link_telegram',
            field=models.URLField(verbose_name='Lien Télégram'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='nb_episode',
            field=models.IntegerField(default=0, verbose_name='Episode'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='nb_season',
            field=models.IntegerField(default=0, verbose_name='Saison'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='quality_audio',
            field=models.CharField(choices=[('BONNE', 'BONNE'), ('MOYENNE', 'MOYENNE'), ('MAUVAISE', 'MAUVAISE'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Qualité Audio'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='quality_video',
            field=models.CharField(choices=[('BONNE', 'BONNE'), ('MOYENNE', 'MOYENNE'), ('MAUVAISE', 'MAUVAISE'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Qualité Vidéo'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='subtitle',
            field=models.CharField(choices=[('OUI', 'OUI'), ('NON', 'NON')], max_length=3, verbose_name='Soutitré ?'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='subtitle_language',
            field=models.CharField(choices=[('FRANÇAIS', 'FRANÇAIS'), ('ANGLAIS', 'ANGLAIS'), ('JAPONAIS', 'JAPONAIS'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Langue du Sous-titre'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='title_tv',
            field=models.CharField(max_length=250, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='voice_language',
            field=models.CharField(choices=[('FRANÇAIS', 'FRANÇAIS'), ('ANGLAIS', 'ANGLAIS'), ('JAPONAIS', 'JAPONAIS'), ('AUCUN', 'AUCUN')], max_length=10, verbose_name='Langue'),
        ),
    ]