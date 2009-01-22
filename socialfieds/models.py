
"""
Models definitions for classifieds.
"""

from django.db import models, IntegrityError
from django.contrib.auth.models import User    
from django.template.defaultfilters import slugify 
from django.utils.translation import ugettext_lazy as _
import re
import datetime
       
CLASSIFIEDS_DAY_LIMIT = 90

class Board(models.Model):
    """
    Board Model
    """

    title     = models.CharField(blank=True, max_length=255)
    slug      = models.SlugField(unique=True,max_length=100, blank=True, null=True) 
    order     = models.PositiveIntegerField(blank=True,  null=True)   
    is_active = models.BooleanField(default=False)
        
    def __unicode__(self):
        return self.title
        
class Category(models.Model):
    """
    Category Model
    """

    title           = models.CharField(blank=True, max_length=255)
    slug            = models.SlugField(unique=True,max_length=100, blank=True, null=True)    
    parent_category = models.ForeignKey('self', null=True, blank=True)
    order           = models.PositiveIntegerField(blank=True,  null=True)
    is_active       = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.title

class ListingManager(models.Manager):
    """
        A basic manager for dealing with Listings.
    """

    def get_latest(self,board=None,category=None,order='-created',user=None):
        """
            Returns latest listings based on age.
            CLASSIFIEDS_DAY_LIMIT is required
            
            method takes the following parameters:        
            ``board``
                Board object. If supplied, method will filter listing from that category.
        
            ``category``
                Category object. If supplied, method will filter listing from that category.
        
            ``order``
                String. If supplied, method sort results by modelfield.
                
            ``user``
                User object. If supplied, method will filter listing from that user.
            
        """
        date_limit = datetime.date.today() - datetime.timedelta(days=CLASSIFIEDS_DAY_LIMIT)
        #TODO: Simplify if statement
        if board and category:
            listings = self.filter(
                                board=board,
                                category=category,
                                is_active=True,
                                user__is_active=True,
                                created__gt=date_limit
                                ).order_by(order)
        elif board is not None and category is None:
            listings = self.filter(
                                board=board,
                                is_active=True,
                                user__is_active=True,                                
                                created__gt=date_limit
                                ).order_by(order)
        elif user is not None:
            listings = self.filter(
                                is_active=True,
                                created__gt=date_limit,
                                user=user,
                                user__is_active=True,                                
                                ).order_by(order)
        else:
            listings = self.filter(
                                is_active=True,
                                created__gt=date_limit,
                                user__is_active=True,                                
                                ).order_by(order)
        return listings

class Listing(models.Model):
    """
        Classified Listing
    """
        
    title       = models.CharField(max_length=255)
    description = models.TextField()
    slug        = models.SlugField(unique=True,max_length=100, blank=True,  null=True)    
    user        = models.ForeignKey(User)
    category    = models.ForeignKey(Category)
    board       = models.ForeignKey(Board)
    created     = models.DateTimeField(default=datetime.datetime.now, )
    edited      = models.DateTimeField(auto_now = True)
    is_active   = models.BooleanField(default=True)
    
    objects = ListingManager()

    def create_slug(self):
        """
            Auto-populate an empty slug field 
            http://www.djangosnippets.org/snippets/761/
        """

        import re
        from django.template.defaultfilters import slugify
    
        if not self.slug:
            self.slug = slugify(self.title) 
    
        while True:
            try:
                super(Listing, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break

    def __unicode__(self):
        return self.title

class ListingFlag(models.Model):
    """
        Model for Listing Flags
    """
    user      = models.ForeignKey(User, related_name="listing_flags")
    listing   = models.ForeignKey(Listing, related_name="flags")
    flag      = models.CharField(max_length=30, db_index=True)
    flag_date = models.DateTimeField(auto_now_add = True)

    #Constants for flag types
    #TODO: Create more relevant flags 
    SUGGEST_REMOVAL = "removal suggestion"
    MODERATOR_DELETION = "moderator deletion"
    MODERATOR_APPROVAL = "moderator approval"

    class Meta:
        unique_together = [('user', 'listing', 'flag')]

    def __unicode__(self):
        return "%s flag of listing ID %s by %s" % \
            (self.flag, self.listing_id, self.user.username)
            
    def save(self, force_insert=False, force_update=False):
        if self.flag_date is None:
            self.flag_date = datetime.datetime.now()
        super(ListingFlag, self).save(force_insert, force_update)
