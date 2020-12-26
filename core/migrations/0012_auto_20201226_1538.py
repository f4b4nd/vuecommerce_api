# Generated by Django 2.2.10 on 2020-12-26 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_orderproduct_discount_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Product__Groups',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Product__SubCategories',
            },
        ),
        migrations.RemoveField(
            model_name='productsubcategory',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.DeleteModel(
            name='ProductSubCategory',
        ),
        migrations.AddField(
            model_name='productgroups',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, related_name='groups', to='core.Product'),
        ),
        migrations.AddField(
            model_name='productgroups',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='core.Topic'),
        ),
    ]