#-*- coding:UTF-8 -*-
import datetime
from django.shortcuts import render, Http404, HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, FormView
from django.views.generic import TemplateView
from django.views.generic.edit import SingleObjectMixin

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy, reverse

from django.contrib import messages
# local
from .models import Annonce, Piece, Tache, Categorie
from .forms import AnnonceForm, SearchForm, TacheForm
from taggit.models import Tag

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

@method_decorator(login_required, 'dispatch')
class TagIndexView(TagMixin, FormView, ListView):
    template_name = 'wejob/annonce_home.html'
    model = Annonce
    paginate_by = '10'
    context_object_name = 'annonces'
    form_class=SearchForm

    def get_queryset(self):
        return Annonce.objects.filter(an_tags__slug=self.kwargs.get('slug'))
    
    def get_success_url(self):
        return reverse('home_annonce')
    

# Create your views here.
@method_decorator(login_required, 'dispatch')
class CreateAnnonceView(CreateView):
    model=Annonce
    form_class=AnnonceForm
    
    def get_success_url(self):
        return reverse('home_annonce')
    
    def get_context_data(self, *args, **kwargs):
        context = super(CreateAnnonceView, self).get_context_data(**kwargs)
        # initialise form avec l'utilisateur connecté
        form = self.get_form()
        form.initial.update(
                            {
                            'owner' : self.request.user,
                            #'titre': self.request.user,
                            })
        
        context['form'] = form
        return context
@method_decorator(login_required, 'dispatch')  
class UpdateAnnonceView(UpdateView):
    model=Annonce
    form_class=AnnonceForm
    template_name = "wejob/annonce_form.html"
    
    def get_success_url(self):
        return reverse('home_annonce')
    
    def get_context_data(self, *args, **kwargs):
        context = super(UpdateAnnonceView, self).get_context_data(**kwargs)
        # initialise form avec l'utilisateur connecté
        form = self.get_form()
        annonce = self.get_object()
        files_attaches = annonce.an_pieces.all()
        context['files_attaches'] = files_attaches
        
        # comment charger les fichiers attachées a cette annonce
        return context
        
@method_decorator(login_required, 'dispatch')
class HomeView(TagMixin, FormView, ListView):
    form_class = SearchForm
    model = Annonce
    template_name = "wejob/annonce_home.html"
    object_list = None
    
    def get_success_url(self):
        return reverse('home_annonce')
     
    def post(self, request, *args, **kwargs):
        #
        context = self.get_context_data(*args, **kwargs)
        cle_search = request.POST.get('requete', None)
        if cle_search :
            context['object_list'] = Annonce.objects.mes_annonces()                             
        #
        else :
            context['object_list']  = Annonce.objects.filter(owner=request.user)
        #
        return self.render_to_response(context)

       
    def get_queryset(self):
       #self.object_list = Annonce.objects.all().order_by('-created')
       return super(HomeView, self).get_queryset().order_by('-an_created')
    
#-----------------------------
# View Tache
#-------------------------
@method_decorator(login_required, 'dispatch')
class CreateTacheView(CreateView):
    # get_context_data()
    form_class = TacheForm
    template_name = "wejob/tache_form.html"
    success_url = reverse_lazy('home_annonce')
    
    def get_object(self, **kwargs):
        self.object = Annonce.objects.get(pk= self.kwargs.get('annonce_pk', None))
        return self.object
        
    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        #form.instance = self.get_object()
        form.initial.update( {'annonce': self.get_object() })
        
        context = super(CreateTacheView, self).get_context_data(*args, **kwargs)
        # on charge le form
        #context['annonce'] = self.get_object()
        
        context['form'] = form
        return context

    def form_valid__(self, form):
        annonce = form.cleaned_data['annonce'] 
        tache = form.save(commit=False)
        tache.annonce = annonce
        tache.save()
        # 
        return HttpResponseRedirect(reverse('home_annonce'))
        
