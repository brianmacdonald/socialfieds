from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import Board, Category, Listing, ListingFlag
from forms import ListingForm, ListingInactivateForm, ListingFlagForm
    
def all_boards(request):
    """Displays all boards"""
    boards = Board.objects.filter(is_active=True).order_by('order')
    template = 'socialfieds/board/all-boards.html'
    data = {'boards':boards,}
    return render_to_response(template, data, context_instance=RequestContext(request))	 	
    
def board_listings(request,slug):
    """Displays all listings in a board"""
    listings = Listing.objects.filter(board=slug, is_active=True)
    template = 'classifieds/board/all-board-listings.html'
    data = {'listings':listings }
    return render_to_response(template, data, context_instance=RequestContext(request))
    
def board_categories(request,slug):
    """Displays all categories and subcategories in a board."""
    board = get_object_or_404(Board, slug=slug, is_active=True)
    categories = Category.objects.filter(is_active=True)\
    			                 .exclude(parent_category=None)\
    			                 .order_by('parent_category__title')
    template = 'socialfieds/board/board.html'
    data = {'board':board, 'categories':categories}
    return render_to_response(template, data, context_instance=RequestContext(request))	
        
def public_listing(request,board_slug,category_slug,listing_slug):
    """Public view of listing"""  
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True)  
    listing = get_object_or_404(Listing,slug=listing_slug, is_active=True)   
    template = 'socialfieds/listing/public.html'
    data = {'listing':listing, 'category':category, 'board':board, }
    return render_to_response(template, data, context_instance=RequestContext(request))	
    
def private_listing(request,board_slug,category_slug,listing_slug=None):
    """Create or edit listing"""
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True)  
    if listing_slug is not None:
        listing = get_object_or_404(Listing,slug=listing_slug, category=category,\
                                 board=board, user=request.user)
    else:
        listing = Listing(category=category, board=board, user=request.user)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            form.instance.create_slug()
            args = form.instance.board.slug, form.instance.category.slug, form.instance.slug
            return HttpResponseRedirect(reverse('public_listing', args=args))
    else:
        form = ListingForm(instance=listing)
    template = 'socialfieds/listing/private.html'
    data = {'listing':listing, 'form':form, 'category':category, 'board':board, }  
    return render_to_response(template, data, context_instance=RequestContext(request))
private_listing = login_required(private_listing)	
     
def inactivate_listing(request, board_slug, category_slug, listing_slug):
    """inactivates listing"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)   
    board = get_object_or_404(Board, slug=board_slug, is_active=True)  
    listing = get_object_or_404(Listing, slug=listing_slug, category=category,\
                                 board=board, user=request.user)
    #TODO: inactivate detection in the template
    inactivated = False
    if request.method == "POST":
        listing = get_object_or_404(Listing, slug=listing_slug, category=category,\
                                 board=board, user=request.user, is_active=True)
        form = ListingInactivateForm(request.POST)
        if form.is_valid():
            listing.is_active = False
            listing.save()
            inactivated = True
    else:
        form = ListingInactivateForm()
    template = 'socialfieds/listing/inactivate.html'
    data = {'listing':listing, 'form':form, 'category':category, 'board':board, 'inactivated':inactivated, }  
    return render_to_response(template, data, context_instance=RequestContext(request))	
inactivate_listing = login_required(inactivate_listing)
    
def catagory_listings(request,board_slug,category_slug):
    """Displays all listings in a category"""
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True) 
    listings = Listing.objects.get_latest(board,category)
    template = 'socialfieds/category/category-listings.html'
    data = {'board':board, 'category':category,'listings':listings, }
    return render_to_response(template, data, context_instance=RequestContext(request))
    
def board_listings(request,slug):
    """Displays all listings in a board"""
    board = get_object_or_404(Board,slug=slug, is_active=True) 
    listings = Listing.objects.filter(board=board,is_active=True)
    template = 'socialfieds/board/board-listings.html'
    data = {'listings':listings, 'board':board, }
    return render_to_response(template, data, context_instance=RequestContext(request))
    
def flag_listing(request,board_slug,category_slug,listing_slug):
    """flags listing for moderation"""
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True)  
    listing = get_object_or_404(Listing,slug=listing_slug, category=category,\
                                 board=board, is_active=True)
    flagged = False
    if request.method == "POST" and request.user.username:
        form = ListingFlagForm(request.POST)
        if form.is_valid():
            flag = ListingFlag(user=request.user,listing=listing,flag="removal suggestion")
            flag.save()
            flagged = True
    else:
        form = ListingFlagForm()
    template = 'socialfieds/listing/flag.html'
    data = {'listing':listing, 'form':form, 'category':category, 'board':board, 'flagged':flagged, }  
    return render_to_response(template, data, context_instance=RequestContext(request))	
