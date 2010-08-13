from django.contrib import admin
from djangerous.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'active')
    search_fields = ('title',)

admin.site.register(Post, PostAdmin)