from django.conrib import admin 
from .models import Publisher, Article, CustomUser
 
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(CustomUser)
