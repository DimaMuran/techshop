# Generated by Django 4.0.3 on 2022-03-13 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='upload_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='upload_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='upload_at',
            new_name='updated_at',
        ),
    ]
