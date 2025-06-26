from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from artikel.models import Kategori, ArtikelBlog
from artikel.forms import KategoriForms, ArtikelForms
from django.contrib.auth.models import User, Group
from .forms import UserEditForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def in_operator(user):
    return user.groups.filter(name='Operator').exists() or user.is_superuser

def artikel_view(request):
    template_name = "artikel.html"
    kategori = Kategori.objects.all()
    artikel = ArtikelBlog.objects.all()
    for k in kategori:
        print(k)

    for a in artikel:
        print(a)


    print(kategori)
    print(artikel)

    context = {
        "title": "Daftar Artikel",
        "kategori": kategori,
        "artikel": artikel
    }
    return render(request, template_name, context)


def detail_artikel(request, id):
    template_name = "detail_artikel.html"
    try :
        artikel = ArtikelBlog.objects.get(id=id)
    except ArtikelBlog.DoesNotExist:
        return redirect(not_found_artikel)
    
    context = {
        "title": "Daftar Artikel",
        "artikel": artikel
    }
    return render(request, template_name, context)

def not_found_artikel(request):
    template_name = "artikel_not_found.html"
    return render(request, template_name,)



################################ admin ###################################3
@login_required(login_url='/auth-login')
def admin_kategori_list(request):
    template_name = "dashboard/admin/kategori_list.html"
    kategori = Kategori.objects.all()
    context ={
        "kategori":kategori
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def admin_kategori_tambah(request):
    template_name = "dashboard/admin/kategori_forms.html"
    if request.method == "POST":
        forms = KategoriForms(request.POST)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user 
            pub.save()
            messages.success(request, 'berhasil tambah kategori')
            return redirect(admin_kategori_list)

    forms = KategoriForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def admin_kategori_update(request, id_kategori):
    template_name = "dashboard/admin/kategori_forms.html"
    kategori = Kategori.objects.get(id=id_kategori)

    if request.method == "POST":
        forms = KategoriForms(request.POST, instance=kategori)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user 
            pub.save()
            messages.success(request, 'berhasil update kategori')
            return redirect(admin_kategori_list)

    forms = KategoriForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def admin_kategori_delete(request, id_kategori):
    try:
        kategori = Kategori.objects.get(id=id_kategori).delete()
        messages.success(request, 'berhasil delete kategori')
    except Kategori.DoesNotExist:
        pass
        messages.erorr(request, 'gagal delete kategori')

    return redirect(admin_kategori_list)


########################## artikel blog #############################
@login_required(login_url='/auth-login')
def admin_artikel_list(request):
    template_name = "dashboard/admin/artikel_list.html"
    artikel = ArtikelBlog.objects.all()
    context ={
        "artikel":artikel
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def admin_artikel_tambah(request):
    template_name = "dashboard/admin/artikel_forms.html"
    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil tambah artikel')
            return redirect(admin_artikel_list)
    else:
        forms = ArtikelForms()
    
    context = {
        "forms": forms
    }
    return render(request, template_name, context)



@login_required(login_url='/auth-login')
def admin_artikel_update(request, id_artikel):
    template_name = "dashboard/admin/artikel_forms.html"
    artikel = ArtikelBlog.objects.get(id=id_artikel)

    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES, instance=artikel)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user 
            pub.save()
            messages.success(request, 'berhasil edit artikel')
            return redirect(admin_artikel_list)

    forms = ArtikelForms(instance=artikel)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def admin_artikel_delete(request, id_artikel):
    try:
        ArtikelBlog.objects.get(id=id_artikel).delete()
        messages.success(request, 'berhasil delete artikel')
    except:
        pass
        messages.error(request, 'gagal delete artikel')

    return redirect(admin_artikel_list)

############################## operator #####################################3

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_list(request):
    template_name = "dashboard/admin/user_list.html"
    daftar_user = User.objects.all()
    context = {
        "daftar_user":daftar_user
    }
    return render(request, template_name, context)


@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_edit(request, user_id):
    template_name = 'dashboard/admin/user_edit.html'
    user = get_object_or_404(User, pk=user_id)
    all_groups = Group.objects.all()
    group_user = []

    for group in user.groups.all():
        group_user.append(group.name)

    all_groups = Group.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        is_staff = request.POST.get("is_staff")
        groups_checked = request.POST.getlist("groups")

        if is_staff is None:
            is_staff = False
        else:
            is_staff = True

        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.groups.set(Group.objects.filter(id__in=groups_checked))
        user.save()

        messages.success(request, f"Berhasil update user {user.username}")
        return redirect('admin_management_user_list') 

    else:
        forms = UserEditForm(instance=user)

    context = {
        'user': user,
        'all_groups': all_groups,
        'group_user': group_user,
        'forms': forms,
    }
    return render(request, template_name, context)