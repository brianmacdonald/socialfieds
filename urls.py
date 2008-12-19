from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import *

urlpatterns = patterns('',
    url(r'^$', view_all_boards, name='all_boards'),  
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/new/$',
        private_post, name='new_post'
        ), 
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/(?P<post_slug>.+)/edit/$',
        private_post, name='edit_post'
        ),
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/(?P<post_slug>.+)/$',
        public_post, name='public_post'
        ),  
    url(r'^(?P<board_slug>.+)/(?P<category_slug>.+)/$',
        view_all_cat_post, name='view_catagory'
        ),
    url(r'^(?P<board_slug>.+)/$', view_board, name='view_board'),

    url(r'^(?P<board_slug>.+)/all/$',view_all_board_post, name='view_all_board'), 
    )