from django.contrib import admin
from models import *

class BoardAdmin(admin.ModelAdmin):
        list_display=('title',)
        ordering = ['order']
        list_per_page = 25
        search_fields = ['title',]
        prepopulated_fields = {'slug':('title',) }

admin.site.register(Board, BoardAdmin)

class CategoryAdmin(admin.ModelAdmin):
        list_display=('title',)
        ordering = ['order']
        list_per_page = 25
        search_fields = ['title',]
        prepopulated_fields = {'slug':('title',) }

admin.site.register(Category, CategoryAdmin)

class ListingAdmin(admin.ModelAdmin):
        list_display=('title', 'created')
        ordering = ['-created']
        list_per_page = 25
        search_fields = ['title', 'description']
        date_hierarchy = 'created'
        prepopulated_fields = {'slug':('title',) }

admin.site.register(Listing, ListingAdmin)

class ListingFlagAdmin(admin.ModelAdmin):
        list_display=('listing', 'flag', 'flag_date')
        ordering = ['-flag_date']
        list_per_page = 25
        search_fields = ['listing', 'flag']
        date_hierarchy = 'flag_date'

admin.site.register(ListingFlag, ListingFlagAdmin)