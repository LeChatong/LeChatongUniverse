# Generated by Django 2.1.1 on 2020-11-18 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beakhub', '0008_auto_20201112_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='BhComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentary', models.TextField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beakhub.BhJob')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beakhub.BhUser')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['created_at'],
            },
        ),
    ]