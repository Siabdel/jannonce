#! -*- coding: utf-8 -*-
"""
Quelques rappels sur le TDD

Pour rappel, la demarche de travail dans le cadre d'une strategie TDD est la suivante :
1- Ecriture des modèles
2- Ecriture des patterns d'URL
3- Creation de quelques donnees de test…
       3.1- Ecriture d'un cas de test
       3.2- Verification que ce cas de test echoue (sinon il ne sert à rien, etant donne que le code n'est pas encore ecrit !)
       3.3- Ecriture du code metier associe
       3.4- Execution du test et verification que tout se passe bien
       
       response.status_code =
        200 : succès de la requête ;
        301 et 302 : redirection, respectivement permanente et temporaire ;
        401 : utilisateur non authentifie ;
        403 : accès refuse ;
        404 : page non trouvee ;
        500 et 503 : erreur serveur.
        !!

"""
from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime
from django.utils import timezone

from django.forms.utils import ValidationError
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse
from django.core.serializers import json, serialize

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .models import Annonce, TypeContrat, Categorie
from django.test import Client
       
class  TestAnnonceCase(TestCase):
    allow_user = True
    
    
    def create_user(self):
        return User.objects.create(first_name='test',
                                   last_name='my_test',
                                   username='test@atlass.fr',
                                   password='1234')
    
    def create_type_contrat(self):
        return TypeContrat.objects.create(libelle='CDD', description='Contrat a duree determinee')
    
    def create_categorie(self):
        return Categorie.objects.create(nom='Informatique', libelle='des annonces pour secteur inforamtique')
    
    def create_annonce(self, **data):
        v_owner = self.create_user()
        v_type_contrat = self.create_type_contrat()
        v_categorie = self.create_categorie()
        #
        return Annonce.objects.create(an_titre=data.get('titre', ""),
                                      owner = v_owner,
                                      an_description= data.get('desc', ""),
                                      an_created=  timezone.now(),
                                      an_salaire= data.get('salaire', 3000),
                                      type_contrat= v_type_contrat,
                                      categorie= v_categorie)
        
    
    def test_post_annonce(self):       
         """
         self.assertTemplateUsed(response, 'journal/article.html')
         """
         data = {'an_titre': 'developpeur python',
         'an_description' : u"recheche un developpeur python experimente plus de 3 ans experience",
         'an_lieu': 'Lyon',
         'an_salaire': '40000',
         'an_type_contrat': self.create_type_contrat(),
         }
         
         
         # test une requete post sur le lien '/annonce/add'
         response  = self.client.post(reverse('add_annonce'),  data, follow=True)
         
         self.failUnlessEqual(response.status_code, 200)

    
 
    def test_annonce_creation(self):
        t_contrat = self.create_type_contrat()
        
        data = {'an_titre': 'developpeur python',
         'an_description' : u"recheche un developpeur python experimente plus de 3 ans experience",
         'an_lieu': 'Lyon',
         'an_salaire': '40000',
         'an_type_contrat': t_contrat,
         }
        
        petite_annonce = self.create_annonce(**data)
        self.assertTrue(isinstance(petite_annonce, Annonce))
        self.assertEqual(petite_annonce.__unicode__(), petite_annonce.an_titre)
    
    def test_list_annonces_view(self):
        petite_annonce = self.create_annonce()
        response = self.client.get(reverse('list_annonces'))
        #self.assertIn(petite_annonce.an_titre, response.content)
        self.assertEqual(response.status_code, 200)
        
            
            
    def test_show_annonce_view(self):
        petite_annonce = self.create_annonce()
        resp = self.client.get(reverse("detail_annonce", kwargs={'pk': petite_annonce.pk}))
       
        self.assertEqual(resp.status_code, 200)
        #self.assertIn(petite_annonce.an_titre, resp.content)
        self.failUnless(isinstance(resp.context['annonce'], Annonce))
        self.assertTemplateUsed(resp, 'wejob/annonce_detail.html')
        
        
    def test_delete_annonce(self):
        petite_annonce = self.create_annonce()
        resp = self.client.get(reverse("delete_annonce", kwargs={'pk': petite_annonce.pk}))
        self.assertEqual(resp.status_code, 200)
       
    def test_edit_annonce(self):
        petite_annonce = self.create_annonce()
        resp = self.client.get(reverse("edit_annonce", kwargs={'pk': petite_annonce.pk}))
        self.assertEqual(resp.status_code, 200)
       
    def test_annonce_home_view(self):
       petite_annonce = self.create_annonce()
       response = self.client.get(reverse('home_annonce'))
       #self.assertIn(petite_annonce.an_titre, response.content)
       self.assertEqual(response.status_code, 200)
      