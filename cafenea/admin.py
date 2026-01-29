'''
Modul ce defineste modul in care modelele aplicatiei sunt inregistrate, vizualizate si gestionate in panoul de administrare Django. Include personalizari pentru raporare rapida si
aspect vizual palcut, editare in lista si protectie a datelor

Aspecte Cheie:
1. **Indicatori vizuali:** - Metoda status_stoc adauga iconite vizuale direct in lista pentru aspect si identificare mai usoara, include de asemenea un script custom "ls/auto_categorie.js'
pentru selectarea automata a categoriei in pagina de administrare Django
2. **Gestionarea Master - Detail:** - Este utilizat 'ElementComandaInLine' (TabularInLine) pentru a permite vizualiarea si adaugarea produselor intr-o comanda direct din pagina comenzii
fara a mai trebui selectata si o categorie separata
3. **Editarea rapida:** - Permite modificarea statusului 'este_activa' din cadrul metodei StireAdmin direct din lista de stiri, eficientizand astfel fluxul de publicare/ascundere al stirilor
4. **Imutabilitate:** - Toate campurile din 'MesajContact' sunt readonl. Lucru care trasnforma interfata intr-un log de audit, prevenind modificarea ccidentala a mesajelor primite de la clienti.
5. **Valori calculate:** - Afiseaza campuri calculate care nu exista direct in baza de date ( precum 'total_afisat' )
'''

from django.contrib import admin
from .models import Angajat, Produs, Client, Comanda, ElementComanda, Stire, MesajContact

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
    list_editable = ('este_activa',) #Permite editarea direct in tabel
    list_filter = ('este_activa', 'creat_la',)
    search_fields = ('titlu', 'continut',)

@admin.register(MesajContact)
class MesajContactAdmin(admin.ModelAdmin):
    list_display = ('nume', 'email', 'subiect', 'data_trimiterii',)
    list_filter = ('data_trimiterii',)
    search_fields = ('nume', 'email', 'subiect', 'mesaj',)
    #Campuri readonly pentru a pastra integritatea mesajelor
    readonly_fields = ('nume', 'email', 'subiect', 'mesaj', 'data_trimiterii',)
