#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
import django

now = django.utils.timezone.now


from django.contrib.auth.models import User
# categorie
class Categorie(models.Model):
    nom = models.CharField(max_length = 50)
    libelle = models.CharField(max_length = 500)
    
    def __unicode__(self):
        return self.nom

# type de contrat
class TypeContrat(models.Model):
    libelle = models.CharField(max_length = 50)
    description = models.TextField(_('Description'), null=True, blank=True)
    
    def __unicode__(self):
        return self.libelle
# la class pieces jointes au annonces et au tache
class Piece(models.Model):
    """
    models :
        les piéces jointes a cette annnce (annonce_id) 
        piece_jointe( libelle, annonce_id, piece)
        
    """
    libelle = models.CharField(max_length = 100)
    fichier = models.FileField(upload_to='upload/')
   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_pieces_for_object(self, obj, distinction=None):
        """
        This function allows you to get pieces for a specific object

        If distinction is set it will filter out any relation that doesnt have
        that distinction.
        
        >>> user = User.objects.get(username='tony')
        >>> try:
        ...     Piece.objects.get_piece_for_object(user)
        ... except Piece.DoesNotExist:
        ...     print("failed")
        ...
        failed

        Now if we add a piece it should return the piece

        >>> piece = Piece(name='My Cal')
        >>> piece.save()
        >>> piece.create_relation(user)
        >>> Piece.objects.get_piece_for_object(user)
        <Piece: My Cal>
        """

        ct = ContentType.objects.get_for_model(obj)
        
        return ct
    
    def __unicode__(self):
        return self.libelle

# la table Annonce d'emploi
TYPE_CONTRAT = ( (1, 'CDD'), (2, 'CDI'),  (3, 'INTERIM'), (4, 'CONTRAT PRO'),  (3, 'CONTRAT'))
class Annonce(models.Model):
    """
    Annonces des job
    models :
        annonce( titre, lieu, salaire, type_contrat, description, reponse, is_active,)
        piece_jointe( libelle, annonce_id, piece)
        
    """
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie   = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    type_contrat = models.ForeignKey(TypeContrat, default=1, on_delete=models.CASCADE)
    an_pieces      = GenericRelation(Piece)
    an_slug = models.SlugField(max_length=255, blank=True)
    an_titre       = models.CharField(_('Titre'), max_length = 100)
    an_description = models.TextField(_('Description'), null=True, blank=True)
    an_lieu        = models.CharField(max_length = 100, null=True, blank=True)
    an_salaire     = models.BigIntegerField(_('Salaire'), blank=True, null=True)
    
    an_entreprise  = models.CharField(_('Entreprise'), max_length = 100)
    an_published   = models.DateField(_('Publiée') , default=datetime.datetime.now())
    
    an_divers      = models.CharField(_('Divers'), max_length = 100, null=True, blank=True)
    an_formation   = models.CharField(_('Formation'), max_length = 100, null=True, blank=True)
    an_connaisannces = models.CharField(max_length = 500, null=True, blank=True)
    an_is_active   = models.BooleanField(_('Active'), default=True,)
    an_created     = models.DateField(_('Créer') , auto_now_add=True)
    an_modified    = models.DateField(_('Modifiée') , auto_now=True)
    an_reponse_employeur = models.TextField(_('Répo    nse employeur'), null=True, blank=True)
    an_tags = TaggableManager()

    def __str(self):
        return self.an_titre

    def __unicode__(self):
        return "%s" % (self.an_slug)
    
    #@models.permalink
    def get_absolute_url(self):
        return ('add_annonce', )
    
    def save(self, **kwargs):
        
        if self.an_titre and not self.an_slug:
            self.an_slug = slugify(self.an_titre)

        super(Annonce, self).save(**kwargs)
    def mes_annonces(self):
        query = self.objects.filter(
                                owner = request.user and
                                Q(an_titre__icontains= cle_search) |
                                Q(an_description__icontains= cle_search)
                                )                                
        #
        return query

# la table Tache d'emploi
class Tache(models.Model):
    """
    models :
        les piéces jointes a cette annnce (annonce_id) 
        piece_jointe( libelle, annonce_id, piece)
    """
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    ta_pieces  = GenericRelation(Piece)
    ta_titre   = models.CharField(max_length = 100)
    ta_close = models.BooleanField(_('Cloturé'), default=False)
    ta_created = models.DateField(_('Date de creation'), auto_now_add=True)
    ta_modified = models.DateField(_('Date de creation'), auto_now=True)
    ta_description = models.TextField(_('Description'), null=True, blank=True)
    
    
    def __unicode__(self):
        return self.ta_titre
    
    #@models.permalink
    def get_absolute_url(self):
        return (reverse('detail_annonce',  kwargs={'pk': self.ta_annonce.id } ))
    
   
    
    
    
        
        