# Generated by Django 2.2.10 on 2021-01-07 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201224_0449'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPaymentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(blank=True, choices=[('S', 'Stripe'), ('P', 'Paypal')], default='S', max_length=1, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=50, null=True)),
                ('one_click_purchasing', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User__PaymentProfile',
                'unique_together': {('user', 'service', 'customer_id')},
            },
        ),
    ]
