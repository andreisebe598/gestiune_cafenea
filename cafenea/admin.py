from django.contrib import admin
from .models import Angajat, Produs, Client, Comanda, ElementComanda, Stire, MesajContact

# Register your models here.
@admin.register(Angajat)
class AngajatAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prenume', 'functie', 'salariu', 'data_angajarii', 'este_angajat')
    list_filter = ('functie', 'este_angajat')
    search_fields = ('nume', 'prenume')

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ('denumire', 'categorie', 'pret_vanzare', 'cantitate', 'status_stoc')
    list_filter = ('categorie', 'denumire')
    search_fields = ('denumire',)

    def status_stoc(self, obj):
        if obj.cantitate == 0:
            return "❎ - Stoc epuizat"
        elif obj.cantitate < 5:
            return "⚠️ - Stoc redus"
        return "✅ Stoc ok!"\
        
    class Media:
        js = ('js/auto_categorie.js',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nume', 'gen', 'varsta', 'bautura_preferata', 'data_inregistrarii')
    list_filter = ('gen', 'bautura_preferata',)
    search_fields = ('nume',)

    def varsta(self, obj):
        return obj.varsta
    varsta.short_description = "Varsta curenta"

class ElementComandaInline(admin.TabularInline):
    model = ElementComanda
    extra = 1

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'angajat', 'data_comenzii', 'total_afisat')
    list_filter = ('data_comenzii', 'angajat')
    inlines = [ElementComandaInline]

    def total_afisat(self, obj):
        return f"{obj.total_comanda} RON"
    total_afisat.short_description = "Total"

@admin.register(Stire)
class StireAdmin(admin.ModelAdmin):
    list_display = ('titlu', 'este_activa', 'data_eveniment', 'creat_la',)
    list_editable = ('este_activa',)
    list_filter = ('este_activa', 'creat_la',)
    search_fields = ('titlu', 'continut',)

@admin.register(MesajContact)
class MesajContactAdmin(admin.ModelAdmin):
    list_display = ('nume', 'email', 'subiect', 'data_trimiterii',)
    list_filter = ('data_trimiterii',)
    search_fields = ('nume', 'email', 'subiect', 'mesaj',)
    readonly_fields = ('nume', 'email', 'subiect', 'mesaj', 'data_trimiterii',)
