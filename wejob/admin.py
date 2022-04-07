#! -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Annonce, ContentType, Piece, Tache, Categorie, TypeContrat
from django.contrib.auth.models import User

# Annonce
class AnnonceAdmin(admin.ModelAdmin):
    #list_display  = ['nom', 'prenom', 'email']
    list_total = [f.name for f in Annonce._meta.get_fields()]
    list_total.remove('tache')
    list_display = list_total
    
    search_fields = ['titre',]

class TacheAdmin(admin.ModelAdmin):
    #list_display  = ['nom', 'prenom', 'email']
    list_display  = [f.name for f in Tache._meta.get_fields()]
    search_fields = ['titre',]

# annonce
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(Tache, TacheAdmin)
admin.site.register(Categorie)
admin.site.register(TypeContrat)
