# Generated by Django 2.2.10 on 2021-01-08 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_userpaymentprofile'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userpaymentprofile',
            unique_together={('user', 'service')},
        ),
    ]