
"""
Models definitions for classifieds.
"""

from django.db import models, IntegrityError
from django.contrib.auth.models import User    
from django.template.defaultfilters import slugify 
import re
       
class Board(models.Model):
    """
    Board Model
    """

    title = models.CharField(blank=True, max_length=255)
    slug = models.SlugField(unique=True,max_length=100, blank=True,  null=True)    
    is_active = models.BooleanField(default=False)
        
    def __unicode__(self):
        return self.title
        
class Category(models.Model):
    """
    Category Model
    """

    title = models.CharField(blank=True, max_length=255)
    slug = models.SlugField(unique=True,max_length=100, blank=True,  null=True)    
    parent_category = models.ForeignKey('self', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

class Post(models.Model):
    """
    Classified Post
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True,max_length=100, blank=True,  null=True)    
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    board = models.ForeignKey(Board)
    created = models.DateTimeField(auto_now_add = True)
    edited = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)
    
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
                super(Post, self).save()
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
