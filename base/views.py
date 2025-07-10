from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .models import Estado, Municipio, Contato, Interesse, Partido, Email, Telephone, Cargo
from django.core.paginator import Paginator
from .forms import ContactForm, EmailFormSet, TelephoneFormSet
import csv
import json
import os
from django.conf import settings



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('cadastrar')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não existe')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('cadastrar')
        else:
            messages.error(request, 'Usuário ou senha incorretos')

    return render(request, 'base/login.html', {'page': 'login'})


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def cadastrarPage(request):
    estados = Estado.objects.all().order_by('nome')
    partidos = Partido.objects.all().order_by('nome')
    cargos = Cargo.objects.all()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST, request.FILES)
        if contact_form.is_valid():
            contact = contact_form.save()

            emails = request.POST.getlist('additional_emails') + [request.POST.get('emails')]
            for email in filter(None, emails):
                Email.objects.create(contact=contact, email=email)

            telefones = request.POST.getlist('additional_telephones') + [request.POST.get('telephones')]
            for telefone in filter(None, telefones):
                Telephone.objects.create(contact=contact, telephone=telefone)

            return redirect('cadastrar')
    else:
        contact_form = ContactForm()

        return render(request, 'base/cadastrar.html', {
            'form': contact_form,
            'estados': estados,
            'partidos': partidos,
            'cargos': cargos
        })



def get_municipios(request, estado_id):
    municipios = Municipio.objects.filter(estado_id=estado_id).values('id', 'nome')
    format_type = request.GET.get('format', 'cadastrar')
    if format_type == 'procurar':
        return JsonResponse(list(municipios), safe=False)
    return JsonResponse({'municipios': list(municipios)}, safe=False)


@login_required(login_url='login')
def procurarPage(request):
    cargo = request.GET.get('cargo')
    estado = request.GET.get('estado')
    municipio = request.GET.get('municipio')
    regiao = request.GET.get('regiao')
    capital = request.GET.get('capital')
    mais_de_80_mil_hab = request.GET.get('mais_de_80_mil_hab')
    regiao_metropolitana = request.GET.get('regiao_metropolitana')
    busca = request.GET.get('busca')
    page = request.GET.get('page', 1)

    contatos = Contato.objects.all()

    if cargo:
        contatos = contatos.filter(cargo_id=cargo)
    if estado:
        contatos = contatos.filter(estado_id=estado)
    if municipio:
        contatos = contatos.filter(municipio_id=municipio)
    if regiao:
        contatos = contatos.filter(municipio__nome_regiao=regiao)
    if capital:
        contatos = contatos.filter(municipio__capital=(capital == "Sim"))
    if mais_de_80_mil_hab:
        contatos = contatos.filter(municipio__mais_de_80_mil_hab=(mais_de_80_mil_hab == "Sim"))
    if regiao_metropolitana:
        contatos = contatos.filter(municipio__regiao_metropolitana=(regiao_metropolitana == "Sim"))
    if busca:
        contatos = contatos.filter(nome__icontains=busca)

    paginator = Paginator(contatos, 10)
    contatos_paginados = paginator.get_page(page)

    context = {
        'contatos': contatos_paginados,
        'cargos_disponiveis': Cargo.objects.all(),
        'estados_disponiveis': Estado.objects.all().order_by('nome'),
        'municipios_disponiveis': Municipio.objects.all(),
        'regioes_disponiveis': Municipio.objects.values('nome_regiao').distinct(),
        'request': request,
    }

    return render(request, 'base/procurar.html', context)


@login_required(login_url='login')
def consulta(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    is_superuser = request.user.is_superuser
    edit_mode = request.GET.get('edit') == '1' and is_superuser

    if request.method == 'POST' and is_superuser:
        form = ContactForm(request.POST, request.FILES, instance=contato)
        if form.is_valid():
            contato = form.save()
            contato.interesses.set(request.POST.getlist('interesses'))
            return redirect('consulta', contato_id=contato.id)
    else:
        form = ContactForm(instance=contato)

    estados = Estado.objects.all().order_by('nome')
    municipios = Municipio.objects.filter(estado=contato.estado) if contato.estado else Municipio.objects.none()
    partidos = Partido.objects.all().order_by('nome')
    interesses = Interesse.objects.all()

    return render(request, 'base/profile.html', {
        'contato': contato,
        'edit_mode': edit_mode,
        'is_superuser': is_superuser,
        'estados': estados,
        'municipios': municipios,
        'partidos': partidos,
        'interesses': interesses,
    })


@login_required(login_url='login')
def exportar_estados_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="estados.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome'])
    for estado in Estado.objects.all():
        writer.writerow([estado.id, estado.nome])
    return response


@login_required(login_url='login')
def exportar_municipios_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="municipios.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome', 'ID_Estado'])
    for municipio in Municipio.objects.all():
        writer.writerow([municipio.id, municipio.nome, municipio.estado_id])
    return response


@login_required(login_url='login')
def exportar_cargos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cargos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome'])
    for cargo in Cargo.objects.all():
        writer.writerow([cargo.id, cargo.nome])
    return response


@login_required(login_url='login')
def exportar_partidos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="partidos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome'])
    for partido in Partido.objects.all():
        writer.writerow([partido.id, partido.nome])
    return response


@login_required(login_url='login')
def mapa_view(request):
    geojson_path = os.path.join(settings.BASE_DIR, 'static', 'geojson', 'grandes_regioes_json.geojson')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        mapa_brasil = json.load(f)

    dados_regioes = [
        {"id": "N", "valor": 10, "nome": "Norte"},
        {"id": "NE", "valor": 20, "nome": "Nordeste"},
        {"id": "CO", "valor": 15, "nome": "Centro-Oeste"},
        {"id": "SE", "valor": 30, "nome": "Sudeste"},
        {"id": "S", "valor": 25, "nome": "Sul"}
    ]

    return render(request, 'base/mapa.html', {
        'mapa_brasil': json.dumps(mapa_brasil),
        'dados_regioes': json.dumps(dados_regioes)
    })
