from django.shortcuts import render, redirect
from artikel.models import Kategori, ArtikelBlog

def artikel_view(request):
    template_name = "landingpage/artikel.html"
    kategori = Kategori.objects.all()
    artikel = ArtikelBlog.objects.all()
    print(request.user)

    context = {
        "title": "Daftar Artikel",
        "kategori": kategori,
        "artikel": artikel
    }
    return render(request, template_name, context)

def not_found_artikel(request):
    template_name = "artikel_not_found.html"
    return render(request, template_name,)

def detail_artikel(request, id):
    template_name = "landingpage/detail.html"
    try :
        artikel = ArtikelBlog.objects.get(id=id)
    except ArtikelBlog.DoesNotExist:
        return redirect(not_found_artikel)
    
    artikel_lainnya = ArtikelBlog.objects.all().exclude(id=id)
       
    context = {
        "title": "Daftar Artikel",
        "artikel": artikel,
        "artikel_lainnya": artikel_lainnya,
    }
    return render(request, template_name, context)


def welcome(request):
    template_name = "index.html"

    context = {
        "title":"selamat datang",

    }
    return render(request, template_name, context)

def kontak(request):
    template_name = "kontak.html"
    context = {
        "title":"kontak"
    }
    return render(request, template_name, context)

def about(request):
    template_name = "about.html"
    context = {
        "title":"about"
    }
    return render(request, template_name, context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/auth-login')

    template_name = "dashboard/index.html"
    context = {
        "title":"selamat datang"
    }
    return render(request, template_name, context)

def artikel_list(request):
    template_name = "dashboard/artikel_list.html"
    context = {
        "title":"selamat datang"
    }
    return render(request, template_name, context)
