# -*- coding:UTF-8 -*-
from django.forms.utils import ErrorList, ValidationError, ErrorDict
from django.template.defaultfilters import slugify
from django import forms
# translate
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

# local

from .models import Annonce, Piece, Tache, Categorie, User

#-----------------------------------
#-- Annonce   
#-----------------------------------
class AnnonceForm(forms.ModelForm):
    piece = forms.FileField(required=False)
    class Meta:
        model   = Annonce
        fields  = "__all__"
       
    
    def save(self):
        annonce =  super(AnnonceForm, self).save()
        # on attache la piece uploader a l'enregistrement de l'annonce
        if self.cleaned_data['piece'] :
            v_piece = self.cleaned_data['piece']
            annonce.an_pieces.create(libelle="ma pice attacheé", fichier=v_piece)
        #
        return annonce
 
class TacheForm(forms.ModelForm):
      
    piece = forms.FileField(required=False)

    class Meta:
        model   = Tache
        fields  = "__all__"
        
    def save(self):
        tache =  super(TacheForm, self).save(commit=False)
        
        if self.cleaned_data.get('annonce', None):
            annonce = self.cleaned_data['annonce']
            tache.annonce = annonce
            tache.save()
        #
        return tache
        

    
#----------------------------------  
#-- formulaire de recherche 
#----------------------------------
class SearchForm( forms.Form ):
   
    requete = forms.CharField(max_length = 100,
                                 label = 'Quoi ?',
                                 help_text = "saisir une cle de recherche", required=False)
    class Meta:
        ordering = ( 'cle', )
