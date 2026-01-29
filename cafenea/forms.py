"""
Fisier ce defineste structura tuturor formularelor utilizare, asigurand validarea datelor introduse de utilizatori

Aspecte Cheie:
1. **Stilizare (Widgets):** - Toate formularele suprascriu widget-urile implicite Django pentru a adauga clase CSS personalizate
                            - Asigura integrarea vizuala cu framework-ul CSS
2. **Extinderea inregistrarii:** - ClientRegistrationForm mosteneste UserCreationForm dar forteaza completarea campurilor 'first_name', 'last_name', si 'email', 
care sunt optionale in mod implicit
3. **Gestionarea profilului:** - Editarea profilului este distribuita in 2 formulare distincte:
                                    - UserUpdateForm pentru datele de autentificare (username, email, nume, prenume)
                                    - ClientUpdateForm pentru datele personale (data nasterii, gen, bautura preferata)
4. **Experienta utilizatorului:** - Utilizeaza type='date' pentru campurile de data, activand astfel selectorul de calendar din browser
"""


from django import forms
from .models import Produs, Client, Angajat, Stire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    """Formular simplu pentru pagina de contact care nu se salveaza direct in DB, doar valideaza"""
    nume = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Numele tau', 'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email-ul tău', 'class': 'form-input'})
    )
    subiect = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Subiect', 'class': 'form-input'})
    )
    mesaj = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Scrie mesajul tău aici...', 'class': 'form-textarea', 'rows': 5})
    )
    
class ProdusForm(forms.ModelForm):
    """Formular folosit pentru gestiunea produselor"""
    class Meta:
        model = Produs
        fields = ['denumire', 'pret_vanzare', 'cost_achizitie', 'cantitate']
        widgets = {
            'denumire': forms.Select(attrs={'class': 'form-input'}),
            'pret_vanzare': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Pret vanzare (RON)'}),
            'cost_achizitie': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Cost achizitie (RON)'}),
            'cantitate': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'placeholder': 'Stoc initial'}),
        }

class ClientRegisterForm(UserCreationForm):
    """Formular custom de inregistrare ce adauga campuri obligatorii (Nume, Prenume, Email) peste UserCreationForm nativ"""
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nume (ex: Popescu)'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Prenume (ex: Ion)'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Adresa de Email'}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']

    def __init__(self, *args, **kwargs):
        """Injecteaza clasa CSS 'form-input' in toate campurile, inclusiv cele native (mostenite)"""
        super(ClientRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input'})


class UserUpdateForm(forms.ModelForm):
    """Formular pentru actualizarea informatiilor de autentificare ale unui client"""
    first_name = forms.CharField(label="Prenume", widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label="Nume", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['gen', 'data_nasterii', 'bautura_preferata']
        widgets = {
            'gen': forms.Select(attrs={'class': 'form-input'}),
            'bautura_preferata': forms.Select(attrs={'class': 'form-input'}),
            'data_nasterii': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

class AngajatForm(forms.ModelForm):
    class Meta:
        model = Angajat
        fields = ['nume', 'prenume', 'functie', 'salariu', 'email', 'telefon', 'data_angajarii', 'data_nasterii', 'este_angajat']
        widgets = {
            'nume': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nume de familie'}),
            'prenume': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Prenume'}),
            'functie': forms.Select(attrs={'class': 'form-input'}),
            'salariu': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'RON'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ex: barista@cafenea.ro'}),
            'telefon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '07xx xxx xxx'}),
            'data_angajarii': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'data_nasterii': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'este_angajat': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class StireForm(forms.ModelForm):
    class Meta:
        model = Stire
        fields = ['titlu', 'continut', 'imagine', 'data_eveniment', 'este_activa']

        widgets = {
            'titlu': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Titlu eveniment sau noutate'}),
            'continut': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Descriere detaliată...'}),
            'imagine': forms.FileInput(attrs={'class': 'form-input'}),
            'data_eveniment': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'este_activa': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }