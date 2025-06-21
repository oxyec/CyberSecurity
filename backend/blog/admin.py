from django.contrib import admin

try:
	from .models import Post
	admin.site.register(Post)
except ImportError:
	# Post model does not exist; handle or log the error as needed
	pass