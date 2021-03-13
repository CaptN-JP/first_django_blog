"""
from django.contrib import admin
from . import models

admin.site.register(models.Post)

	#registers Post database to the default database provided by django"""


#To customize the model's layout on admin page :

from django.contrib import admin
from .models import Post	

class PostAdmin(admin.ModelAdmin):
	fieldsets=[
	("Title/Date", {"fields":["title", "date_posted"]}),
	("Content", {"fields":["author", "content"]}),
	]

admin.site.register(Post,PostAdmin)

"""here we are overriding the PostAdmin(<modelname>Admin) which gets created 
by default.
# Instead of writing the above line of code, we can use a decorator:

	@admin.register(Post)
	class PostAdmin(admin.ModelAdmin):
		pass

"""