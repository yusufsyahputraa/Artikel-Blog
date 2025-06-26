from django.contrib import admin
from artikel.models import Kategori, ArtikelBlog
# Register your models here.


class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama', 'created_at','created_by']
    search_fields = ['nama']
admin.site.register(Kategori, KategoriAdmin)


class ArtikelBlogAdmin(admin.ModelAdmin):
    list_display = ['kategori', 'judul', 'status', 'created_at','created_by']
    search_fields = ['judul']
admin.site.register(ArtikelBlog, ArtikelBlogAdmin)