from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import Board, Category, Post
from forms import PostForm

def view_board(request,board_slug):
    """Displays all categories and subcategories in a board."""
    board = get_object_or_404(Board,slug=board_slug, is_active=True)
    categories = Category.objects.filter(is_active=True).exclude(parent_category=None)
    template = 'classifieds/board/board.html'
    data = {'board':board, 'categories':categories }
    return render_to_response(template, data, context_instance=RequestContext(request))	  

def view_all_boards(request):
    """Displays all boards"""
    boards = Board.objects.filter(is_active=True)
    template = 'classifieds/board/all-boards.html'
    data = {'boards':boards }
    return render_to_response(template, data, context_instance=RequestContext(request))	 	
        
def public_post(request,board_slug,category_slug,post_slug):
    """Public view of post"""  
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True)  
    post = get_object_or_404(Post,slug=post_slug, is_active=True)   
    template = 'classifieds/post/public.html'
    data = {'post':post, 'category':category, 'board':board, }
    return render_to_response(template, data, context_instance=RequestContext(request))	

@login_required 
def private_post(request,board_slug,category_slug,post_slug=None):
    """Create or edit post"""
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True)  
    if post_slug is not None:
        post = get_object_or_404(Post,slug=post_slug, category=category,\
                                 board=board, user=request.user)
    else:
        post = Post(category=category, board=board, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            form.instance.create_slug()
            args = form.instance.board.slug, form.instance.category.slug, form.instance.slug
            return HttpResponseRedirect(reverse('public_post', args=args))
    else:
        form = PostForm(instance=post)
    template = 'classifieds/post/private.html'
    data = {'post':post, 'form':form, 'category':category, 'board':board, }  
    return render_to_response(template, data, context_instance=RequestContext(request))	
    
def view_all_cat_post(request,board_slug,category_slug):
    """Displays all posts in a category"""
    category = get_object_or_404(Category,slug=category_slug, is_active=True)   
    board = get_object_or_404(Board,slug=board_slug, is_active=True) 
    posts = Post.objects.filter(category=category,is_active=True)
    template = 'classifieds/category/all-cat-posts.html'
    data = {'board':board, 'category':category,'posts':posts }
    return render_to_response(template, data, context_instance=RequestContext(request))

def view_all_board_post(request,board_slug):
    """Displays all posts in a board"""
    posts = Post.objects.filter(board=board_slug,is_active=True)
    template = 'classifieds/board/all-board-posts.html'
    data = {'posts':posts }
    return render_to_response(template, data, context_instance=RequestContext(request))