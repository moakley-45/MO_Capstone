from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Recipe)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('notes', 'ingredients', 'method',)

    def get_summernote_options(self, request, context):
        options = super().get_summernote_options(request, context)
        options['toolbar'] = [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
            ['checkbox', ['checkbox']], 
        ]
        return options

    class Media:
        js = ('admin/js/custom_admin.js',)
