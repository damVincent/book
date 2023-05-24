from django.contrib import admin
from django.utils.html import format_html

from home.models import Author, Book, BookReview, Genre, Publisher, Message

class BookInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('preview_cover_image',)

    def preview_cover_image(self, obj):
        return format_html('<img src="{}" alt="Cover Image" style="max-height: 200px;"/>', obj.cover_image.url)

    preview_cover_image.short_description = 'Cover Image Preview'

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(BookReview)
admin.site.register(Message)
