# Generated by Django 2.2.10 on 2021-01-07 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20201226_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at'], 'verbose_name': 'Product__Comment'},
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='method',
            new_name='service',
        ),
    ]
