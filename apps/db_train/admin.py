from django.contrib import admin
from .models import Author, AuthorProfile, Tag, Entry

admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Tag)
admin.site.register(Entry)
