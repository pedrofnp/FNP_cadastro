from django.contrib import admin
from .models import Estado, Municipio,  Contato, Partido, Email, Telephone, Cargo

# Register your models here.

class EmailInline(admin.TabularInline):
    model = Email
    extra = 1  # Number of empty forms to display

class TelephoneInline(admin.TabularInline):
    model = Telephone
    extra = 1  # Number of empty forms to display

class ContatoAdmin(admin.ModelAdmin):
    inlines = [EmailInline, TelephoneInline]

admin.site.register(Estado)
admin.site.register(Partido)
admin.site.register(Municipio)
admin.site.register(Cargo)
admin.site.register(Contato, ContatoAdmin)
