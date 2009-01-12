from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import *


urlpatterns = patterns('',

    url(r'^$', all_boards, name='all_boards'),
      
    url(r'^(?P<slug>.+)/all/$',board_listings, name='board_listings'), 
        
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/new/$',
        private_listing, name='new_listing'
        ), 
        
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/(?P<listing_slug>.+)/edit/$',
        private_listing, name='edit_listing'
        ),
        
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/(?P<listing_slug>.+)/inactivate/$',
        inactivate_listing, name='inactivate_listing'
        ),    
        
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/(?P<listing_slug>.+)/flag/$',
        flag_listing, name='flag_listing'
        ),   
        
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/(?P<listing_slug>.+)/$',
        public_listing, name='public_listing'
        ),  
        
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/$',
        catagory_listings, name='catagory_listings'
        ),
        
    url(r'^(?P<slug>.+)/$', board_categories, name='board_categories'),
        
    )