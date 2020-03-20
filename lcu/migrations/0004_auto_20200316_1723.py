# Generated by Django 2.1.1 on 2020-03-16 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcu', '0003_auto_20200313_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='recieve_mail',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_parent_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email_sender',
            field=models.EmailField(max_length=150, null=True, verbose_name='email_sender'),
        ),
    ]