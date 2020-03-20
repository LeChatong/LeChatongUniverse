# Generated by Django 2.1.1 on 2020-03-11 16:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lcu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='movie_detail',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='tv_detail',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='updated_at'),
        ),
    ]