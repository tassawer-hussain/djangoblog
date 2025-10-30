from django.contrib import admin
from .models import Post

# admin.site.register(Post)

# Register your models here.
@admin.register(Post) # this decorator performs the same as admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
	# used in admin panel to display the fields
	list_display = ['title', 'slug', 'author', 'publish', 'status']
	list_filter = ['status', 'created', 'publish', 'author'] # used to filter the fields
	search_fields = ['title', 'body'] # used to search the fields
	prepopulated_fields = {'slug': ('title',)} # used to populate the slug field from the title field
	raw_id_fields = ['author'] # used to display the author field as a search instead of a dropdown
	date_hierarchy = 'publish' # used to display the publish field as a dropdown
	ordering = ['status', 'publish'] # used to order the fields
	show_facets = admin.ShowFacets.ALWAYS # used to show the facets in the admin panel. make sure facet filters are always displayed - Filter counts is the number of items in the filter
