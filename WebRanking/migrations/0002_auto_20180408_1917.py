# Generated by Django 2.0.4 on 2018-04-08 17:16

from django.db import migrations
import requests
import re

""" This function migrates the database with the best chess players according to the website 
    https://www.prochessleague.com/players.html using the requests library to get a string version
    of the website and then by using regular expressions to find the names and ratings of each player
"""

def add_players(apps, schema_editor):
    Player = apps.get_model('rankings', 'Player')
    web_page = requests.get('https://www.prochessleague.com/players.html')
    text_page = web_page.text
    start = text_page.find("const inputData")
    end = text_page.find("];", start)
    data = text_page[start:end]
    name_filter = re.compile(">(.+)</a>")
    rating_filter = re.compile("'Rating':\s'(\d+)'")
    per_filter = re.compile("'Perf':\s'(\d+|-)'")
    names = name_filter.findall(data)
    ratings = rating_filter.findall(data)
    performances = per_filter.findall(data)

    for i in range(0, len(names)):
        if performances[i]=="-":    #Some of the players in the site don't have their performances listed so they get the default value of 2000
            Player(name=names[i], ranking=int(ratings[i]), performances=2000).save()
        else:
            Player(name=names[i], ranking=int(ratings[i]), performances=int(performances[i])).save()

class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_players),
    ]