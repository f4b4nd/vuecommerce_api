# Generated by Django 2.2.10 on 2020-12-24 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201221_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('1', 'M.'), ('2', 'Mme'), ('3', 'Autre')], max_length=1, null=True),
        ),
    ]
