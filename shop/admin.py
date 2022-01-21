from django.contrib import admin

from shop.models import Genre, Book, Writer, MediaType


class WriterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class MediaTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(MediaType, MediaTypeAdmin)
