# Generated by Django 4.1 on 2022-08-19 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_categorymain_cat_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymain',
            name='cat_main_img',
            field=models.ImageField(blank=True, upload_to='Category/cat_main_img'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('cat_sub_img', models.ImageField(blank=True, upload_to='Category/cat_sub_img')),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.categorymain')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
                'ordering': ['sub_category_name'],
            },
        ),
    ]