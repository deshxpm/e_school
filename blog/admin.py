from django.contrib import admin

# Register your models here.
from.models import *

admin.site.register(Post)
admin.site.register(Tag)
# admin.site.register(Category)
admin.site.register(PostAuthor)
admin.site.register(Image)