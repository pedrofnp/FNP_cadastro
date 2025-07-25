import os
import json
import csv
import requests
from functools import lru_cache
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Estado, Contato, Interesse, Partido, Email, Telephone, Cargo
from .forms import ContactForm


# ======================================
# Função utilitária local para carregar JSON
# ======================================
def carregar_dados_json(nome_arquivo='db_sqmunicipio.json'):
    caminhos_possiveis = [
        os.path.join(settings.BASE_DIR, 'static', 'data', nome_arquivo),
        os.path.join(settings.BASE_DIR, 'base', nome_arquivo),
    ]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
    raise FileNotFoundError(f'Arquivo {nome_arquivo} não encontrado.')


# ======================================
# Lógica API + fallback local
# ======================================
@lru_cache(maxsize=500)
def consultar_status_municipio(nome_municipio):
    nome_normalizado = nome_municipio.strip().upper()

    # Primeiro: tenta buscar na API do Google (adimplentes 2025)
    try:
        url_api = "https://script.google.com/macros/s/AKfycbxSqtjXeAbMcCdH3rAFO3V6V6W3qt3a3rPaZQidtiLyN2-y0fNCHUCBZu-WO9DzMbAcIQ/exec"
        response = requests.get(url_api, timeout=10)
        if response.status_code == 200:
            municipios_api = response.json()
            for m in municipios_api:
                if m["municipio"].strip().upper() == nome_normalizado:
                    m["adimplente"] = True
                    return m
    except Exception as e:
        print(f"[ERRO API] {e}")

    # Segundo: tenta buscar no JSON local
    try:
        dados_json = carregar_dados_json()
        municipio = next(
            (m for m in dados_json if m["municipio"].strip().upper() == nome_normalizado),
            None
        )
        if municipio:
            municipio["adimplente"] = False
            return municipio
    except Exception as e:
        print(f"[ERRO JSON] {e}")

    # Se não encontrar, retorna padrão
    return {
        "municipio": nome_municipio,
        "uf": "",
        "populacao": None,
        "adimplente": False
    }


# ======================================
# View MAPA
# ======================================
@login_required(login_url='login')
def mapaPage(request):
    municipios = carregar_dados_json()
    return render(request, 'base/mapa.html', {'municipios': municipios})


# ======================================
# API info município (por nome)
# ======================================
def municipio_info_api(request, nome_municipio):
    try:
        dados = consultar_status_municipio(nome_municipio)
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)


# ======================================
# LOGIN / LOGOUT
# ======================================
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
        if user:
            login(request, user)
            return redirect('cadastrar')
        else:
            messages.error(request, 'Usuário ou senha incorretos')
    return render(request, 'base/login.html', {'page': 'login'})


def logoutUser(request):
    logout(request)
    return redirect('login')


# ======================================
# CADASTRO
# ======================================
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
        municipios = carregar_dados_json()

    return render(request, 'base/cadastrar.html', {
        'form': contact_form,
        'estados': estados,
        'partidos': partidos,
        'cargos': cargos,
        'municipios_disponiveis': municipios,
    })


# ======================================
# PÁGINA DE BUSCA (ATUALIZADA)
# ======================================
@login_required(login_url='login')
def procurarPage(request):
    cargo = request.GET.get('cargo')
    estado = request.GET.get('estado')
    municipio = request.GET.get('municipio')
    busca = request.GET.get('busca')
    page = request.GET.get('page', 1)

    contatos = Contato.objects.all()
    if cargo:
        contatos = contatos.filter(cargo_id=cargo)
    if estado:
        contatos = contatos.filter(estado_id=estado)
    if municipio:
        contatos = contatos.filter(municipio__nome=municipio)
    if busca:
        contatos = contatos.filter(nome__icontains=busca)

    paginator = Paginator(contatos, 10)
    contatos_paginados = paginator.get_page(page)

    # Lista única de municípios da página atual
    municipios_pagina = set(c.municipio.nome.strip() for c in contatos_paginados)
    status_municipios = {}
    for nome in municipios_pagina:
        status_municipios[nome] = consultar_status_municipio(nome)

    context = {
        'contatos': contatos_paginados,
        'cargos_disponiveis': Cargo.objects.all(),
        'estados_disponiveis': Estado.objects.all().order_by('nome'),
        'status_municipios': status_municipios,
        'request': request,
    }

    return render(request, 'base/procurar.html', context)


# ======================================
# CONSULTA PERFIL
# ======================================
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
            messages.success(request, 'Alterações salvas com sucesso.')
            return HttpResponseRedirect(reverse('consulta', args=[contato.id]))
        else:
            messages.error(request, 'Erro ao salvar alterações.')
    else:
        form = ContactForm(instance=contato)

    estados = Estado.objects.all().order_by('nome')
    partidos = Partido.objects.all().order_by('nome')
    interesses = Interesse.objects.all()
    emails = Email.objects.filter(contact=contato)
    telefones = Telephone.objects.filter(contact=contato)
    foto_existe = contato.foto and contato.foto.name and contato.foto.storage.exists(contato.foto.name)
    cargos = Cargo.objects.all()

    municipios = carregar_dados_json()

    return render(request, 'base/profile.html', {
        'contato': contato,
        'edit_mode': edit_mode,
        'is_superuser': is_superuser,
        'estados': estados,
        'municipios': municipios,
        'partidos': partidos,
        'interesses': interesses,
        'emails': emails,
        'telefones': telefones,
        'foto_existe': foto_existe,
        'cargos': cargos,
    })


# ======================================
# API LISTAGEM DE MUNICÍPIOS
# ======================================
def get_municipios(request, estado_id=None):
    municipios = carregar_dados_json()
    if estado_id:
        municipios = [m for m in municipios if m['uf'].lower() == estado_id.lower()]

    format_type = request.GET.get('format', 'cadastrar')
    if format_type == 'procurar':
        return JsonResponse(municipios, safe=False)
    return JsonResponse({'municipios': municipios}, safe=False)


# ======================================
# EDITAR MUNICÍPIO
# ======================================
@login_required(login_url='login')
def editar_municipio(request):
    municipios_data = carregar_dados_json()
    municipio_selecionado = None

    if request.method == 'POST':
        nome_municipio = request.POST.get('municipio_nome')
        adimplente_novo = request.POST.get('adimplente') == 'on'

        for m in municipios_data:
            if m['municipio'].lower() == nome_municipio.lower():
                m['adimplente'] = adimplente_novo
                break

        path = os.path.join(settings.BASE_DIR, 'static', 'data', 'db_sqmunicipio.json')
        if not os.path.exists(path):
            path = os.path.join(settings.BASE_DIR, 'base', 'db_sqmunicipio.json')

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(municipios_data, f, ensure_ascii=False, indent=2)

        messages.success(request, f'Município "{nome_municipio}" atualizado com sucesso.')

    elif request.method == 'GET' and 'municipio_nome' in request.GET:
        nome_municipio = request.GET.get('municipio_nome')
        for m in municipios_data:
            if m['municipio'].lower() == nome_municipio.lower():
                municipio_selecionado = m
                break

    return render(request, 'base/editar_municipio.html', {
        'municipios': sorted(municipios_data, key=lambda x: x['municipio']),
        'municipio_selecionado': municipio_selecionado
    })


# ======================================
# EXPORTAÇÃO
# ======================================
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
