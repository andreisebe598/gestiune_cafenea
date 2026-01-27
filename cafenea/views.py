from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Count, Q
from django.contrib import messages
from django.contrib.auth import login
from .forms import ContactForm, ProdusForm, ClientRegisterForm, ClientUpdateForm, UserUpdateForm, AngajatForm, StireForm
from .models import Comanda, Produs, ElementComanda, Angajat, Stire, MesajContact, Client
from django.contrib.auth.decorators import login_required, user_passes_test
from .cart import Cart

# functie helper pentru a verifica daca utilizatorul este manager sau superuser
def este_manager(user):
    return user.is_staff or user.is_superuser

# view simplu pentru randarea template-ului de baza
def base(request):
    return render(request, 'base.html')

# ==================== PAGINI PUBLICE ====================

# pagina principala a site-ului
def main(request):
    # preia ultimele 3 stiri active pentru a le afisa pe prima pagina
    stiri = Stire.objects.filter(este_activa=True)[:3]
    # preia primul produs din categoria 'cafele' pentru a-l afisa ca produs vedeta
    produs_vedeta = Produs.objects.filter(categorie='Cafele').first()
    
    context = {
        'stiri': stiri,
        'produs_vedeta': produs_vedeta,
    }
    return render(request, 'main.html', context)

# pagina de meniu cu toate produsele
def menu(request):
    # preia toate produsele din baza de date
    produse = Produs.objects.all()
    # defineste categoriile manual pentru iterare in template
    categorii = ['Cafele', 'Bauturi Calde', 'Bauturi Reci', 'Soft Drinks', 'Dulciuri']

    context = {
        'produse': produse,
        'categorii': categorii,
    }
    return render(request, 'menu.html', context)

# pagina despre noi / echipa
def about(request):
    # preia toti angajatii pentru a-i afisa la sectiunea echipa
    echipa = Angajat.objects.all() 
    
    context = {
        'echipa': echipa
    }
    return render(request, 'about.html', context)

# pagina de contact cu formular
def contact(request):
    # verifica daca formularul a fost trimis prin metoda post
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # salveaza mesajul in baza de date
            MesajContact.objects.create(
                nume=form.cleaned_data['nume'],
                email=form.cleaned_data['email'],
                subiect=form.cleaned_data['subiect'],
                mesaj=form.cleaned_data['mesaj']
            )
            
            # afiseaza mesaj de succes si reincarca pagina
            messages.success(request, f"Multumim, {form.cleaned_data['nume']}! Mesajul a fost salvat.")
            return redirect('contact')
    else:
        # afiseaza formular gol pentru metoda get
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

# ==================== AUTENTIFICARE SI PROFIL ====================

# inregistrare utilizator nou
def register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            # salveaza user-ul in baza de date django
            user = form.save() 
            
            # autentifica utilizatorul automat dupa inregistrare
            login(request, user)
            messages.success(request, f"Bine ai venit, {user.first_name}! Contul a fost creat.")
            return redirect('menu')
    else:
        form = ClientRegisterForm()

    return render(request, 'register.html', {'form': form})

# pagina de profil a utilizatorului
@login_required
def profil(request):
    try:
        # incearca sa obtina profilul de client existent
        client_existent = request.user.client
    except Client.DoesNotExist:
        # daca nu exista, il creeaza pe loc
        Client.objects.create(
            user=request.user, 
            nume=f"{request.user.last_name} {request.user.first_name}" or request.user.username,
            gen='Nespecificat'
        )

    if request.method == 'POST':
        # formulare pentru actualizare date user si client
        u_form = UserUpdateForm(request.POST, instance=request.user)
        c_form = ClientUpdateForm(request.POST, instance=request.user.client)

        if u_form.is_valid() and c_form.is_valid():
            user = u_form.save()
            client = c_form.save(commit=False)
            
            # sincronizeaza numele complet
            client.nume = f"{user.last_name} {user.first_name}"
            client.save()
            
            messages.success(request, 'Profilul tau a fost actualizat!')
            return redirect('profil')

    else:
        # pre-completeaza formularele cu datele existente
        u_form = UserUpdateForm(instance=request.user)
        c_form = ClientUpdateForm(instance=request.user.client)

    # preia istoricul comenzilor pentru utilizatorul curent
    comenzi_istoric = request.user.client.comenzi.all().order_by('-data_comenzii')

    context = {
        'u_form': u_form,
        'c_form': c_form,
        'comenzi': comenzi_istoric
    }

    return render(request, 'profil.html', context)

# ==================== COS DE CUMPARATURI ====================

# adauga produs in cos
def cart_add(request, produs_id):
    cart = Cart(request)
    produs = get_object_or_404(Produs, id=produs_id)
    cart.add(produs_id=produs.id)
    messages.success(request, f'{produs.get_denumire_display()} a fost adaugat in cos.')
    return redirect('menu') 

# sterge produs din cos
def cart_remove(request, produs_id):
    cart = Cart(request)
    produs = get_object_or_404(Produs, id=produs_id)
    cart.remove(produs_id)
    messages.warning(request, f'{produs.get_denumire_display()} a fost sters din cos.')
    return redirect('cart_detail')

# afiseaza detaliile cosului
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

# finalizare comanda
@login_required
def checkout(request):
    cart = Cart(request)
    
    # verifica daca cosul este gol
    if len(cart) == 0:
        messages.warning(request, "Cosul tau este gol.")
        return redirect('menu')

    # verifica stocul pentru fiecare produs din cos
    for item in cart:
        produs = item['product']
        cantitate_ceruta = item['cantitate']
        
        if produs.cantitate < cantitate_ceruta:
            messages.error(request, f"Stoc insuficient pentru {produs.get_denumire_display()}. Disponibil: {produs.cantitate}.")
            return redirect('cart_detail')

    # identifica sau creeaza profilul de client
    try:
        client = request.user.client
    except:
        client = Client.objects.create(user=request.user, nume=request.user.username)

    # asigneaza un angajat virtual pentru comanda online
    angajat_online = Angajat.objects.filter(nume='Comenzi', prenume='Online').first()
    if not angajat_online:
        angajat_online = Angajat.objects.first()

    # creeaza comanda in baza de date
    comanda_noua = Comanda.objects.create(
        client=client,
        angajat=angajat_online
    )

    # muta produsele din cos in baza de date
    for item in cart:
        ElementComanda.objects.create(
            comanda=comanda_noua,
            produs=item['product'],
            cantitate=item['cantitate']
        )

    # goleste cosul si afiseaza mesaj de succes
    cart.clear()
    messages.success(request, f"Comanda #{comanda_noua.id} a fost plasata cu succes!")
    
    return redirect('profil')

# ==================== DASHBOARD MANAGER ====================

# dashboard cu rapoarte si statistici
@login_required
@user_passes_test(este_manager)
def dashboard_rapoarte(request):
    # calculeaza total incasari si cheltuieli folosind agregari
    date_financiare = ElementComanda.objects.aggregate(
        total_incasari = Sum(F('cantitate') * F('produs__pret_vanzare')),
        total_cheltuieli = Sum(F('cantitate') * F('produs__cost_achizitie'))
    )

    incasari = date_financiare['total_incasari'] or 0
    cheltuieli = date_financiare['total_cheltuieli'] or 0
    profit = incasari - cheltuieli

    # calculeaza marja de profit procentuala
    marja = (profit / incasari * 100) if incasari > 0 else 0

    # determina top 5 cele mai vandute produse
    top_produse = Produs.objects.annotate(
        total_vandut = Sum('elementcomanda__cantitate')
    ).filter(total_vandut__gt=0).order_by('-total_vandut')[:5]

    # calculeaza performanta angajatilor dupa numarul de comenzi
    performanta_angajati = Angajat.objects.annotate(
        nr_comenzi = Count('comenzi_procesate')
    ).order_by('-nr_comenzi')

    context = {
        'incasari': incasari,
        'cheltuieli': cheltuieli,
        'profit': profit,
        'marja_profit': marja,
        'top_produse': top_produse,
        'performanta_angajati': performanta_angajati
    }

    return render(request, 'dashboard.html', context)

# ==================== GESTIUNE PRODUSE ====================

# lista de gestiune produse
@login_required
@user_passes_test(este_manager)
def lista_gestiune_produse(request):
    # afiseaza toate produsele ordonate dupa categorie si nume
    produse = Produs.objects.all().order_by('categorie', 'denumire')
    return render(request, 'gestiune_produse.html', {'produse': produse})

# adaugare produs nou
@login_required
@user_passes_test(este_manager)
def adauga_produs(request):
    if request.method == 'POST':
        form = ProdusForm(request.POST)
        if form.is_valid():
            produs_nou = form.save(commit=False)
            
            # verifica daca produsul exista deja pentru a actualiza stocul
            produs_existent = Produs.objects.filter(denumire=produs_nou.denumire).first()
            
            if produs_existent:
                produs_existent.cantitate += produs_nou.cantitate
                produs_existent.pret_vanzare = produs_nou.pret_vanzare
                produs_existent.cost_achizitie = produs_nou.cost_achizitie
                produs_existent.save()
                messages.info(request, f'Stoc actualizat pentru {produs_nou.get_denumire_display()}.')
            else:
                produs_nou.save()
                messages.success(request, 'Produs nou adaugat in inventar!')
            
            return redirect('lista_gestiune_produse')
    else:
        form = ProdusForm()

    return render(request, 'adauga_produs.html', {'form': form})

# modificare produs existent
@login_required
@user_passes_test(este_manager)
def modifica_produs(request, pk):
    produs = get_object_or_404(Produs, pk=pk)

    if request.method == 'POST':
        form = ProdusForm(request.POST, instance=produs)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produsul "{produs.get_denumire_display()}" a fost actualizat.')
            return redirect('lista_gestiune_produse')
    else:
        form = ProdusForm(instance=produs)

    return render(request, 'modifica_produs.html', {'form': form, 'produs': produs})

# stergere produs
@login_required
@user_passes_test(este_manager)
def sterge_produs(request, pk):
    produs = get_object_or_404(Produs, pk=pk)
    if request.method == 'POST':
        nume = produs.get_denumire_display()
        produs.delete()
        messages.warning(request, f'Produsul "{nume}" a fost sters din baza de date.')
        return redirect('lista_gestiune_produse')
    
    return redirect('lista_gestiune_produse')

# ==================== GESTIUNE ANGAJATI ====================

# lista de gestiune angajati
@login_required
@user_passes_test(este_manager)
def lista_gestiune_angajati(request):
    # afiseaza angajatii, intai cei activi
    angajati = Angajat.objects.all().order_by('-este_angajat', 'nume') 
    return render(request, 'gestiune_angajati.html', {'angajati': angajati})

# adaugare angajat nou
@login_required
@user_passes_test(este_manager)
def adauga_angajat(request):
    if request.method == 'POST':
        form = AngajatForm(request.POST, request.FILES)
        if form.is_valid():
            angajat = form.save()
            messages.success(request, f'Bun venit in echipa, {angajat.prenume}!')
            return redirect('lista_gestiune_angajati')
    else:
        form = AngajatForm()

    return render(request, 'adauga_angajat.html', {'form': form})

# modificare angajat existent
@login_required
@user_passes_test(este_manager)
def modifica_angajat(request, pk):
    angajat = get_object_or_404(Angajat, pk=pk)

    if request.method == 'POST':
        form = AngajatForm(request.POST, request.FILES, instance=angajat)
        if form.is_valid():
            form.save()
            messages.success(request, f'Datele angajatului {angajat.nume} au fost actualizate.')
            return redirect('lista_gestiune_angajati')
    else:
        form = AngajatForm(instance=angajat)

    return render(request, 'modifica_angajat.html', {'form': form, 'angajat': angajat})

# stergere angajat
@login_required
@user_passes_test(este_manager)
def sterge_angajat(request, pk):
    angajat = get_object_or_404(Angajat, pk=pk)
    if request.method == 'POST':
        nume = f"{angajat.nume} {angajat.prenume}"
        angajat.delete()
        messages.warning(request, f'Angajatul {nume} a fost sters din sistem.')
        return redirect('lista_gestiune_angajati')
    
    return redirect('lista_gestiune_angajati')

# ==================== GESTIUNE COMENZI ====================

# lista de gestiune comenzi cu cautare
@login_required
@user_passes_test(este_manager)
def lista_gestiune_comenzi(request):
    # preia toate comenzile ordonate descrescator dupa data
    comenzi = Comanda.objects.all().order_by('-data_comenzii')
    
    # verifica parametrul de cautare din url
    search_query = request.GET.get('q', '') 
    
    if search_query:
        # cauta dupa id daca este numar, altfel dupa nume client
        if search_query.isdigit():
            comenzi = comenzi.filter(
                Q(id=search_query) | 
                Q(client__nume__icontains=search_query)
            )
        else:
            comenzi = comenzi.filter(client__nume__icontains=search_query)

    context = {
        'comenzi': comenzi,
        'search_query': search_query 
    }
    
    return render(request, 'gestiune_comenzi.html', context)

# vizualizare detalii comanda stil bon fiscal
@login_required
@user_passes_test(este_manager)
def detalii_comanda(request, pk):
    comanda = get_object_or_404(Comanda, pk=pk)
    return render(request, 'detalii_comanda.html', {'comanda': comanda})

# stergere comanda
@login_required
@user_passes_test(este_manager)
def sterge_comanda(request, pk):
    comanda = get_object_or_404(Comanda, pk=pk)
    if request.method == 'POST':
        id_comanda = comanda.id
        comanda.delete()
        messages.warning(request, f'Comanda #{id_comanda} a fost stersa definitiv.')
        return redirect('lista_gestiune_comenzi')
    
    return redirect('lista_gestiune_comenzi')

# ==================== GESTIUNE STIRI ====================

@login_required
@user_passes_test(este_manager)
def lista_gestiune_stiri(request):
    # Le ordonam dupa data crearii (cele mai noi sus)
    stiri = Stire.objects.all().order_by('-creat_la')
    return render(request, 'gestiune_stiri.html', {'stiri': stiri})

# 2. ADAUGA STIRE
@login_required
@user_passes_test(este_manager)
def adauga_stire(request):
    if request.method == 'POST':
        # ATENTIE: request.FILES este obligatoriu pentru upload imagini!
        form = StireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Știrea a fost publicată cu succes!')
            return redirect('lista_gestiune_stiri')
    else:
        form = StireForm()

    return render(request, 'adauga_stire.html', {'form': form})

# 3. MODIFICA STIRE
@login_required
@user_passes_test(este_manager)
def modifica_stire(request, pk):
    stire = get_object_or_404(Stire, pk=pk)

    if request.method == 'POST':
        form = StireForm(request.POST, request.FILES, instance=stire)
        if form.is_valid():
            form.save()
            messages.success(request, f'Știrea "{stire.titlu}" a fost actualizată.')
            return redirect('lista_gestiune_stiri')
    else:
        form = StireForm(instance=stire)

    return render(request, 'modifica_stire.html', {'form': form, 'stire': stire})

# 4. STERGE STIRE
@login_required
@user_passes_test(este_manager)
def sterge_stire(request, pk):
    stire = get_object_or_404(Stire, pk=pk)
    if request.method == 'POST':
        stire.delete()
        messages.warning(request, 'Știrea a fost ștearsă definitiv.')
        return redirect('lista_gestiune_stiri')
    
    return redirect('lista_gestiune_stiri')