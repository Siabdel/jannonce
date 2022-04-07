#-*- coding:UTF-8 -*-
'''
Models file for the `products` coleman app. These models represent
basic product and catalog information for an ecommerce
application. They are designed to be pluggable and reusable in any
Django project.
'''
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib import admin
from django.urls import reverse_lazy, reverse
from .models import Annonce, Tache
from .forms import AnnonceForm
from .views import CreateAnnonceView, UpdateAnnonceView, HomeView, TagIndexView
from .views import CreateTacheView
from django.urls import path

urlpatterns = [
    
    path('home/', HomeView.as_view(), name='home_annonce'),
    path('tag/<slug:title>/', TagIndexView.as_view(), name='tagged'),

     
    path('add/',  CreateAnnonceView.as_view(), name='add_annonce'),
    path('view/<pk>/', DetailView.as_view(model=Annonce), name='detail_annonce'),
    path('del/<pk>/',  DeleteView.as_view(model=Annonce, success_url="/wejob/list"),        
        name='delete_annonce'),

    path('list/', ListView.as_view(model=Annonce, queryset=Annonce.objects.all(),
                                     paginate_by=20, template_name='annonce_list.html'),
                                     name='list_annonces' ),
    path('edit/<pk>/', UpdateAnnonceView.as_view(),
        name='edit_annonce'),
    #------------------------------------
    #-- les actions sur annonce ==> Taches
    #fields = '__all__'
    #------------------------------------
    path('tache/add/<annonce_pk>',  CreateTacheView.as_view(), name='add_tache'),
    path('tache/edit/<pk>',  UpdateView.as_view(model=Tache,
                                                         success_url="/wejob/home/",
                                                         fields="__all__"), name='edit_tache'),
    path('tache/del/<pk>',  DeleteView.as_view(model=Tache, success_url="/wejob/home/"),
                        name='del_tache'),
    path('tache/show/<pk>',  DetailView.as_view(model=Tache), name='show_tache'),
   
]





"""
    path('edit/(?P<pk>\d+)/$',  UpdateView.as_view(model=Annonce, form_class=AnnonceForm,
                                                    template_name='annonce_form.html' )),
    path('view/(?P<pk>\d+)/$',  DetailView.as_view(model=Annonce,
                                                    template_name='annonce_details.html' )),
    path('del/(?P<pk>\d+)/$', DeleteView.as_view(model=Annonce,success_url=reverse_lazy('list_art'),
                                                  template_name='annonce_confirm_delete.html')),
"""