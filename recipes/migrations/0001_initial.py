# Generated by Django 2.2.6 on 2020-11-06 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('units', models.CharField(max_length=50, verbose_name='Единицы измерения')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_value', to='recipes.Ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='Recepie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('image', models.ImageField(upload_to='recepies/', verbose_name='Фото')),
                ('description', models.TextField(verbose_name='Описание')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('breakfast', models.BooleanField(verbose_name='Завтрак')),
                ('lunch', models.BooleanField(verbose_name='Обед')),
                ('dinner', models.BooleanField(verbose_name='Ужин')),
                ('сooking_time', models.PositiveSmallIntegerField(verbose_name='Время приготовления')),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_recepie', to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(through='recipes.IngredientValue', to='recipes.Ingredients', verbose_name='Ингридиенты')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='ingredientvalue',
            name='recepie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepie_value', to='recipes.Recepie'),
        ),
    ]