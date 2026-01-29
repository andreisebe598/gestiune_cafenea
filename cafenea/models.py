"""
Modul ce defineste structura bazei de date si regulile fundamnetale ale aplicatiei. Modelele sunt interconectate pentru a gestiona fluxul de date complet: Stoc -> Personal -> Clienti -> Vanzari

Aspecte Cheie:
1. **Gestiunea inteligenta a produselor:**
        - Autocategorisire: Metoda save() este suprascrisa pentru a detecta automat categoria bazat pe numele produsului 
        - Structura ierarhica: Foloseste tuple imbricate in 'DENUMIRE_CHOICES' pentru a grupa produsele logic in interfata de administrare
2. **Sistem inteligent de comenzi:**
        - Relatia 'Comanda' -> 'ElementComanda'
        - Validarea stocului: Nu permite salvarea unei linii daca cantitatea ceruta depaseste stocul disponibil
        - Scaderea automata: La salvarea ElementComanda, cantitatea este scazuta automat din stocul 'Produsului'
3. **Extensia profilului user:**
        - Implementeaza relatia de tip 1-la-1 cu modelul standard Django 'User'
        - Campuri calculate: Propritatea 'varsta' este calculata automat in functie de data nasterii
        - Filtrare relationala: Campul 'bautura_preferata' exclude automat produsele din categoria 'Dulciuri' folosind 'Q objects'
4. **Sistem de resurse umane:**
        - Gestioneaza starea angajatului (Activ/Inactiv) printr-un boolean, pastrand istoricul angajatilor chiar si dupa plecarea acestora
"""


from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models  import Q

# ==================== MODEL ANGAJAT ====================
class Angajat(models.Model):
    FUNCTII = [
        ('Barista', 'Barista'),
        ('Casier', 'Casier'),
        ('Administrator', 'Administrator'),
        ('Director', 'Director')
    ]

    nume=models.CharField(max_length=100)
    prenume=models.CharField(max_length=100)
    functie=models.CharField(max_length=100, choices=FUNCTII)
    salariu=models.DecimalField(max_digits=10, decimal_places=2)

    email = models.EmailField(unique=True, null=True, blank=True)
    telefon = models.CharField(max_length=15, unique=True, null=True, blank=True)

    data_angajarii = models.DateField(default=timezone.now)
    data_nasterii = models.DateField(null=True, blank=True)

    este_angajat =  models.BooleanField(
        default=True,
        help_text='Bifat in cazul in care angajatul este activ, debifat in cazul in care angajatul a demisionat'
    )

    def __str__(self):
        status = "Activ" if self.este_angajat else "Inactiv"
        return f"{self.nume} {self.prenume} - {self.get_functie_display()} -> {self.salariu} RON ({status})"
    
    class Meta:
        verbose_name_plural = 'Angajati'

# ==================== MODEL PRODUS ====================
class Produs(models.Model):
    CATEGORII = [
        ('Cafele', 'Cafele'),
        ('Bauturi Calde', 'Bauturi Calde'),
        ('Bauturi Reci', 'Bauturi Reci'),
        ('Soft Drinks', 'Soft Drinks'),
        ('Dulciuri', 'Dulciuri')
    ]


    DENUMIRE_CHOICES = [
        ('Cafele', (
            ('Espresso', 'Espresso'), ('Espresso Lung', 'Espresso Lung'),
            ('Espresso Decaf', 'Espresso Decaf'), ('Espresso Machiatto', 'Espresso Machiatto'),
            ('Espresso Con Panna', 'Espresso Con Panna'), ('Americano', 'Americano'),
            ('Cappuccino', 'Cappuccino'), ('Caffe Latte', 'Caffe Latte'), ('Flat White', 'Flat White'),
        )),
        ('Bauturi Calde', (
            ('Ciocolata calda', 'Ciocolata calda'), ('Chai latte', 'Chai latte'), ('Ceai', 'Ceai'),
        )),
        ('Bauturi Reci', (
            ('Iced Coffee', 'Iced Coffee'), ('Greek Frappe', 'Greek Frappe'),
            ('Ness Frappe', 'Ness Frappe'), ('Espresso Tonic', 'Espresso Tonic'),
            ('Milkshake', 'Milkshake'), ('Smoothie', 'Smoothie'),
        )),
        ('Soft Drinks', (
            ('Coca-Cola', 'Coca-Cola'), ('Fanta', 'Fanta'), ('Sprite', 'Sprite'),
            ('Pepsi', 'Pepsi'), ('Apa Plata', 'Apa Plata'), ('Apa Minerala', 'Apa Minerala'),
            ('RedBull', 'RedBull'),
        )),
        ('Dulciuri', (
            ('Negresa', 'Negresa'), ('Fursec American', 'Fursec American'),
            ('Briosa', 'Briosa'), ('Biscuite cu ovaz', 'Biscuite cu ovaz'),
            ('Mini Croissant', 'Mini Croissant'), ('Biscuiti Vegani', 'Biscuiti Vegani'),
            ('Salam de Biscuiti', 'Salam de Biscuiti'), ('Ciocolata de Casa', 'Ciocolata de Casa'),
        )),
    ]

    denumire = models.CharField(max_length=100, choices=DENUMIRE_CHOICES)
    categorie = models.CharField(max_length=50, choices=CATEGORII, blank=True) 
    pret_vanzare = models.DecimalField(max_digits=10, decimal_places=2) 
    cost_achizitie = models.DecimalField(max_digits=10, decimal_places=2) 
    cantitate = models.IntegerField(default=0) 

    def save(self, *args, **kwargs):
        """La salvare, determina automat categoria produsului pe baza denumirii selectate"""
        for cat_nume, produse_tuple in self.DENUMIRE_CHOICES:
            nume_produse = [p[0] for p in produse_tuple]
            if self.denumire in nume_produse:
                self.categorie = cat_nume
                break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_denumire_display()} ({self.get_categorie_display()})"
    
    class Meta:
        verbose_name_plural = 'Produse'

# ==================== MODEL CLIENT ====================
class Client(models.Model):
    """on_delete = CASCADE inseamna ca daca stergi userul se sterge si profilul de Client"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    GENURI = [
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
        ('Nespecificat', 'Nespecificat'),
    ]

    nume = models.CharField(max_length=100)
    
    gen = models.CharField(max_length=20, choices=GENURI, default='Nespecificat')
    
    data_nasterii = models.DateField(null=True, blank=True)

    bautura_preferata = models.ForeignKey(
        'Produs',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fani',
        limit_choices_to=~Q(categorie='Dulciuri') # Nu permite selectarea dulciurilor
    )

    data_inregistrarii = models.DateTimeField(auto_now_add=True)

    @property
    def varsta(self):
        """Calculeaza varsta curenta in functie de data_nasterii"""
        if self.data_nasterii:
            today = timezone.now().date()
            return today.year - self.data_nasterii.year - (
                (today.month, today.day) < (self.data_nasterii.month, self.data_nasterii.day)
            )
        return "N/A"
    
    def __str__(self):
        user_str = f" [User: {self.user.username}]" if self.user else ""
        return f"{self.nume}{user_str} ({self.gen}, {self.varsta} ani) -> {self.bautura_preferata}"

    class Meta:
        verbose_name_plural = 'Clienti'
        
# ==================== MODEL COMANDA ====================
class Comanda(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='comenzi')
    angajat = models.ForeignKey('Angajat', on_delete=models.CASCADE, related_name='comenzi_procesate')
    data_comenzii = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comenzi'

    def __str__(self):
        return f"Comanda {self.id} - Client: {self.client.nume} - Angajat: {self.angajat.nume} {self.angajat.prenume} ({self.data_comenzii.strftime('%d.%m.%Y %H:%M')})"

    @property
    def total_comanda(self):
        return sum(item.subtotal for item in self.elemente.all())

class ElementComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='elemente')
    produs = models.ForeignKey('Produs', on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField(default=1)

    def clean(self):
        """Validare: nu permite salvarea daca stocul e insuficient"""
        if not self.pk:
            if self.produs.cantitate < self.cantitate:
                raise ValidationError({
                    'cantitate': f"Stoc insuficient pentru {self.produs.denumire}. Stoc disponibil: {self.produs.cantitate}"
                })

    @property
    def subtotal(self):
        return self.produs.pret_vanzare * self.cantitate
    
    def save(self, *args, **kwargs):
        """La salvare (creare) scade automat cantitatea din stoc"""
        if not self.pk:
            self.produs.cantitate -= self.cantitate
            self.produs.save()

        super().save(*args, **kwargs)

# ==================== MODEL STIRI ( pt main page ) ====================
class Stire(models.Model):
    titlu = models.CharField(max_length=200)
    continut = models.TextField(verbose_name='Descriere eveniment/noutate')
    imagine = models.ImageField(upload_to='noutati/', null=True, blank=True)
    data_eveniment = models.DateField(null=True, blank=True)
    este_activa = models.BooleanField(default=True)
    creat_la = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Stiri'
        ordering = ['-creat_la']
    
    def __str__(self):
        return self.titlu
    
# ==================== MODEL FORMULAR CONTACT ====================
class MesajContact(models.Model):
    nume = models.CharField(max_length=100)
    email = models.EmailField()
    subiect = models.CharField(max_length=150)
    mesaj = models.TextField()
    data_trimiterii = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Mesaje Contact'
        ordering = ['-data_trimiterii']

    def __str__(self):
        return f"{self.nume} - {self.subiect}"