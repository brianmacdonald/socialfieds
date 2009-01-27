__test__ = {"SOCIALFIEDS_TESTS": r"""

  ###################
  ### Model Tests ###
  ###################

>>> import datetime
>>> from django.contrib.auth.models import User
>>> from models import Board, Category, Listing, ListingFlag
>>> now = datetime.datetime.now()

# create a user to associate to the listing
>>> user = User.objects.create_user("brianm", "brian.m17@gmail.com", password='password')

# Create listing objects
>>> board = Board.objects.create(
...     title='Naples', slug='naples',order=1,is_active=True
... )
>>> parent_category = Category.objects.create(
...     title='Jobs', parent_category='',order=1,is_active=True,
... )
>>> category = Category.objects.create(
...     title='Web Development',slug='web-development',parent_category=parent_category,
...     order=1,is_active=True,
... )
>>> Listing.objects.create(
...     title='Web Developer',description='We need a django developer!',
...      user=user, category=category, board=board, created=now-datetime.timedelta(days=3)
... )
<Listing: Web Developer>

>>> Listing.objects.create(
...     title='Ruby on Rails Developer',
...     description='We need a Ruby on Rails developer!', user=user,
...     category=category, board=board, created=now-datetime.timedelta(days=2)
... )
<Listing: Ruby on Rails Developer>

>>> board = Board.objects.create(
...     title='Bonita Springs',order=2, is_active=True
... )
>>> category = Category.objects.create(
...     title='Web Design',parent_category=parent_category,
...     order=1,is_active=True,
... )
>>> Listing.objects.create(
...     title='Web Designer', description='Must know XHTML/CSS!',
...     user=user, category=category, board=board, created=now-datetime.timedelta(days=1)
... )
<Listing: Web Designer>

# get all listings
>>> Listing.objects.get_latest()
[<Listing: Web Designer>, <Listing: Ruby on Rails Developer>, <Listing: Web Developer>]

# get just latest from 'Bonita Springs' board
>>> board = Board.objects.get(pk=2)
>>> Listing.objects.get_latest(board)
[<Listing: Web Designer>]

# get just latest from 'Naples' board and 'Web Development' category
>>> board = Board.objects.get(pk=1)
>>> category = Category.objects.get(pk=2)
>>> Listing.objects.get_latest(board,category)
[<Listing: Ruby on Rails Developer>, <Listing: Web Developer>]

# get just latest from just the user
>>> Listing.objects.get_latest(user=user)
[<Listing: Web Designer>, <Listing: Ruby on Rails Developer>, <Listing: Web Developer>]

# create Listing moderation flag
>>> listing = Listing.objects.get(pk=1)
>>> ListingFlag.objects.create(user=user,listing=listing,flag='Removal Suggestion')
<ListingFlag: Removal Suggestion flag of listing ID 1 by brianm>

  #################
  ### URL Tests ###
  #################

# url tests
>>> from django.core.urlresolvers import reverse
>>> from django.test.client import Client

>>> c = Client()
>>> c.login(username='brianm', password='password')
True

>>> reverse('all_boards')
'/'
>>> board = Board.objects.get(pk=1)
>>> reverse('board_listings', kwargs={'slug': board.slug,} )
'/naples/all/'
>>> board = Board.objects.get(pk=1)
>>> reverse('board_listings', kwargs={'slug': board.slug,} )
'/naples/all/'
>>> category = Category.objects.get(pk=2)
>>> url = reverse('new_listing',
...     kwargs={'board_slug': board.slug,'category_slug': category.slug,}
... )
>>> response = c.post(url, 
...     {'title' : 'ASP Developer',
...     'description' : 'I would like to find a ASP Developer'}
... )

>>> Listing.objects.latest('created')
<Listing: ASP Developer>

>>> listing = Listing.objects.latest('created')
>>> reverse('public_listing',
...     kwargs={'board_slug': board.slug,'category_slug': category.slug,
...     'listing_slug' : listing.slug,}
... )
'/naples/web-development/asp-developer/'

# edit latest
>>> url = reverse('edit_listing',
...     kwargs={'board_slug': board.slug,'category_slug': category.slug, 
...     'listing_slug' : listing.slug,}
... )
>>> response = c.post(url, 
...     {'title' : 'ASP.net Developer', 
...     'description' : 'I would really like to find a ASP.net Developer'}
... )
>>> Listing.objects.latest('created')
<Listing: ASP.net Developer>

# inactivate latest
>>> url = reverse('inactivate_listing',
...     kwargs={'board_slug': board.slug,'category_slug': category.slug, 
...     'listing_slug' : listing.slug,}
... )
>>> response = c.post(url, 
...     {'inactivate' : 'True',}
... )
>>> Listing.objects.latest('created').is_active
False

# flag latest
>>> url = reverse('inactivate_listing',
...     kwargs={'board_slug': board.slug,'category_slug': category.slug, 
...     'listing_slug' : listing.slug,}
... )
>>> response = c.post(url, 
...     {'flag' : 'True',}
... )
>>> ListingFlag.objects.latest('flag_date')
<ListingFlag: Removal Suggestion flag of listing ID 1 by brianm>

"""}