# Generated by Django 2.2.6 on 2020-11-06 08:13

from django.db import migrations
import json

def code(apps, schema_editor):
    Ingredients = apps.get_model('recipes', 'Ingredients')
    
    with open('ingredients.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)    
        
    for ingredient in data:
        Ingredients.objects.create(
            name=ingredient['title'], units=ingredient['dimension']
        )

    
def reverse_code(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code, reverse_code=reverse_code),
    ]