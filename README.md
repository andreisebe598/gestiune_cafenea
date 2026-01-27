 # ☕ Sistem de Management pentru Cafenea

Un sistem web complet pentru gestionarea operațiunilor unei cafenele moderne, dezvoltat cu Django. Aplicația acoperă tot ce ține de managementul inventarului, comenzilor clienților și administrarea personalului.

## 📋 Cuprins

- [Despre Proiect](#despre-proiect)
- [Funcționalități](#funcționalități)
- [Tehnologii Utilizate](#tehnologii-utilizate)
- [Instalare](#instalare)
- [Configurare](#configurare)
- [Utilizare](#utilizare)
- [Structura Proiectului](#structura-proiectului)
- [Modele de Date](#modele-de-date)
- [Capturi de Ecran](#capturi-de-ecran)
- [Contribuții](#contribuții)
- [Licență](#licență)

## 🎯 Despre Proiect

Acest sistem a fost dezvoltat pentru a digitaliza și eficientiza operațiunile unei cafenele moderne. Oferă o soluție completă de management care include funcționalități pentru clienți (vizualizare meniu, comandă online) și pentru administrație (gestiune stocuri, personal, rapoarte financiare).

Aplicația separă interfața publică de cea administrativă, oferind o experiență optimizată atât pentru clienți, cât și pentru managementul afacerii.

## ✨ Funcționalități

### Pentru Clienți

- **Autentificare & Înregistrare**: Sistem complet de autentificare cu funcționalitate de resetare parolă
- **Meniu Interactiv**: Navigare ușoară prin produse organizate pe categorii (Cafele, Băuturi Calde, Băuturi Reci, Soft Drinks, Dulciuri)
- **Coș de Cumpărături**: Sistem de coș bazat pe sesiune care persistă între vizite
- **Profil Personal**: Gestionarea datelor personale, preferințe și istoric comenzi
- **Plasare Comenzi Online**: Verificare automată a stocurilor și confirmare instantanee
- **Pagină de Contact**: Formular pentru întrebări și feedback

### Pentru Administrare

- **Dashboard Centralizat**: Vedere de ansamblu cu rapoarte financiare și statistici
  - Total încasări vs cheltuieli
  - Profit net
  - Top 5 produse cele mai vândute
  - Statistici angajați
  
- **Gestiune Produse**:
  - Adăugare/editare/ștergere produse
  - Actualizare automată stocuri la fiecare comandă
  - Tracking cost achiziție vs preț vânzare
  - Categorii predefinite și validare

- **Gestiune Angajați**:
  - Evidență completă personal (Barista, Casier, Administrator, Director)
  - Date contact și salarizare
  - Status activ/inactiv
  - Tracking date angajare și naștere

- **Gestiune Comenzi**:
  - Vizualizare toate comenzile cu detalii
  - Căutare după ID sau nume client
  - Export detalii comandă (stil bon fiscal)
  - Posibilitate de anulare comenzi

- **Gestiune Știri/Evenimente**:
  - Publicare noutăți pe pagina principală
  - Upload imagini pentru evenimente
  - Activare/dezactivare știri
  - Planificare evenimente viitoare

## 🛠 Tehnologii Utilizate

### Backend
- **Python 3.x** - Limbaj principal
- **Django 4.x** - Framework web
- **SQLite** - Bază de date (ușor de migrat către PostgreSQL/MySQL)

### Frontend
- **HTML5 & CSS3** - Structură și stilizare
- **JavaScript** - Interactivitate client-side
- **Django Templates** - Sistem de template-uri

### Biblioteci & Tools
- **Django Signals** - Crearea automată a profilurilor la înregistrare
- **Django Forms** - Validare și procesare formulare
- **Django Auth** - Sistem de autentificare și permisiuni
- **Pillow** - Procesare imagini

## 📦 Instalare

### Cerințe Preliminare

```bash
Python 3.8+
pip (Python package manager)
virtualenv (opțional, dar recomandat)
```

### Pași de Instalare

1. **Clonează repository-ul**
```bash
git clone https://github.com/username/cafenea-management.git
cd cafenea-management
```

2. **Creează un mediu virtual**
```bash
python -m venv venv
source venv/bin/activate  # Pe Windows: venv\Scripts\activate
```

3. **Instalează dependențele**
```bash
pip install -r requirements.txt
```

4. **Configurează baza de date**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Creează un superuser**
```bash
python manage.py createsuperuser
```

6. **Colectează fișierele statice**
```bash
python manage.py collectstatic
```

7. **Pornește serverul de dezvoltare**
```bash
python manage.py runserver
```

Aplicația va fi disponibilă la `http://127.0.0.1:8000/`

## ⚙️ Configurare

### Setări Importante

În `settings.py`, configurează următoarele:

```python
# Securitate
SECRET_KEY = 'your-secret-key-here'
DEBUG = False  # în producție
ALLOWED_HOSTS = ['yourdomain.com']

# Bază de date (opțional - PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cafenea_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Configurare Email (pentru resetare parolă)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 📖 Utilizare

### Acces Administrator

1. Accesează `/admin/` pentru panoul Django Admin
2. Autentifică-te cu credențialele de superuser
3. Sau accesează `/dashboard/` pentru dashboard-ul personalizat

### Primul Setup

1. **Adaugă un angajat special pentru comenzi online**:
   - Nume: `Comenzi`
   - Prenume: `Online`
   - Funcție: `Administrator`
   - Acest angajat va fi asociat automat comenzilor online

2. **Populează meniul**:
   - Accesează `Gestiune → Produse → Adaugă Produs Nou`
   - Completează detaliile produsului
   - Categoria se atribuie automat în funcție de denumire

3. **Publică prima știre**:
   - Accesează `Gestiune → Știri → Adaugă Știre Nouă`
   - Adaugă o imagine și descriere
   - Marchează ca activă pentru a apărea pe pagina principală

### Fluxul unei Comenzi

1. **Client**: Navighează în meniu și adaugă produse în coș
2. **Client**: Accesează coșul și finalizează comanda
3. **Sistem**: Verifică stocurile automat
4. **Sistem**: Scade cantitățile din inventar
5. **Sistem**: Creează înregistrarea comenzii
6. **Administrator**: Poate vedea comanda în dashboard sau în `Gestiune → Comenzi`

## 📁 Structura Proiectului

```
📂 proiect_final_django/
 ├── 📂 gestiune_cafenea/       # Configurații nucleu
 ├── 📂 cafenea/               # Aplicația principală (App)
 │    ├── 📂 migrations        # Migrări bază de date
 │    ├── 📂 static/           # Fișiere statice (CSS, JS, imagini)
 │    ├── 📂 templates         # Template-uri HTML
 │    ├── cart.py              # Logica de sesiune pentru coș
 │    ├── signals.py           # Automatizări de profil (Signals)
 │    ├── models.py            # Schema DB și logică de stoc
 │    ├── views.py             # Controller & Dashboard Manager
 │    ├── forms.py             # Formulare custom și validări
 │    └── urls.py              # Rutele specifice aplicației
 ├── 📂 media/                 # Fișiere încărcate de utilizatori
 │    ├── 📂 noutati           # Imagini stiri
 ├── manage.py                 # Script management Django
 ├── requirements.txt          # Dependențele proiectului
 └── .gitignore                # Excluderi (venv, pycache, .env)
```

## 🗄 Modele de Date

### Angajat
Stochează informații despre personalul cafenelei.

```python
- nume, prenume
- functie (Barista, Casier, Administrator, Director)
- salariu
- email, telefon
- data_angajarii, data_nasterii
- este_angajat (activ/inactiv)
```

### Produs
Gestionează inventarul cafenelei.

```python
- denumire (choices predefinite)
- categorie (se atribuie automat)
- pret_vanzare, cost_achizitie
- cantitate (stoc)
```

**Categorii disponibile**:
- Cafele (Espresso, Cappuccino, Americano, etc.)
- Băuturi Calde (Ciocolată caldă, Chai Latte, Ceai)
- Băuturi Reci (Iced Coffee, Frappe, Smoothie, etc.)
- Soft Drinks (Coca-Cola, Fanta, Sprite, etc.)
- Dulciuri (Negresă, Croissant, Cookies, etc.)

### Client
Profiluri utilizatori conectate la Django User.

```python
- user (OneToOneField cu User)
- nume
- gen (Masculin, Feminin, Nespecificat)
- data_nasterii
- bautura_preferata (ForeignKey către Produs)
- data_inregistrarii
```

### Comanda & ElementComanda
Sistemul de comenzi cu detalii complete.

```python
Comanda:
- client (ForeignKey)
- angajat (ForeignKey)
- data_comenzii
- total_comanda (property calculat)

ElementComanda:
- comanda (ForeignKey)
- produs (ForeignKey)
- cantitate
- subtotal (property calculat)
```

### Stire
Știri și evenimente afișate pe homepage.

```python
- titlu
- continut
- imagine
- data_eveniment
- este_activa
- creat_la
```

### MesajContact
Mesaje primite prin formularul de contact.

```python
- nume, email
- subiect, mesaj
- data_trimiterii
```

## 🔐 Securitate & Permisiuni

### Decoratori Utilizați

- `@login_required` - Restricționează accesul la utilizatori autentificați
- `@user_passes_test(este_manager)` - Verifică dacă utilizatorul este staff sau superuser

### Protecție CSRF

Toate formularele includ token-uri CSRF pentru protecție împotriva atacurilor cross-site request forgery.

### Validări

- Verificare stoc înainte de plasarea comenzii
- Validare email unic pentru angajați
- Validare telefon unic
- Sanitizare input-uri formulare

## 🚀 Features Avansate

### Cart System (Coș de Cumpărături)

Implementat folosind sesiuni Django, coșul persistă între vizite și suportă:
- Adăugare multiplă a aceluiași produs
- Ștergere produse individuale
- Calcul automat preț total
- Sincronizare cu stocul disponibil

### Django Signals

La crearea unui utilizator nou, se generează automat un profil Client asociat folosind `post_save` signals.

### Auto-categorization

Categoria produsului se atribuie automat în funcție de denumire la salvare, eliminând erorile umane.

### Dashboard Analytics

Calcule în timp real folosind agregări Django ORM:
- `Sum()` pentru totale
- `F()` pentru calcule la nivel de rând
- `Count()` pentru statistici
- `annotate()` pentru grupări complexe

## 📊 Rapoarte & Analytics

Dashboard-ul oferă:

1. **Rezumat Financiar**
   - Total încasări din vânzări
   - Total cheltuieli cu achiziții
   - Profit net (încasări - cheltuieli)

2. **Top Produse**
   - Top 5 produse după cantitate vândută
   - Include produs, cantitate și venit generat

3. **Statistici Angajați**
   - Total angajați activi
   - Total angajați inactivi
   - Totalul salariilor lunare

4. **Activitate Comenzi**
   - Număr total comenzi
   - Comenzi recente cu detalii

## 🎨 Design & UX

### Principii de Design

- **Mobile-First**: Design responsive pentru toate dispozitivele
- **Intuitive Navigation**: Meniu clar și consistent
- **Feedback Visual**: Mesaje de succes/eroare pentru toate acțiunile
- **Clean Interface**: Accent pe conținut, fără distrageri

### Mesaje Utilizator

Sistem complet de mesaje Django pentru feedback:
- `messages.success()` - Acțiuni reușite
- `messages.error()` - Erori și probleme
- `messages.warning()` - Avertismente
- `messages.info()` - Informații generale

## 🧪 Testing

### Manual Testing Checklist

- [ ] Înregistrare utilizator nou
- [ ] Login/Logout
- [ ] Resetare parolă
- [ ] Adăugare produse în coș
- [ ] Plasare comandă
- [ ] Verificare scădere stoc
- [ ] Acces dashboard ca admin
- [ ] CRUD operații pentru fiecare model
- [ ] Formulare de contact
- [ ] Publicare știri

### Test Scenarios

1. **Stoc Insuficient**: Încearcă să comanzi mai mult decât există în stoc
2. **Comenzi Simultane**: Doi clienți comandă același produs cu stoc limitat
3. **Validare Email**: Încearcă să adaugi doi angajați cu același email
4. **Permisiuni**: Încearcă să accesezi dashboard fără drepturi admin

## 🔄 Îmbunătățiri Viitoare

Funcționalități planificate pentru versiunile următoare:

- [ ] **Sistem de Plată Online**: Integrare Stripe/PayPal
- [ ] **Notificări Email**: Confirmări comenzi automate
- [ ] **Rapoarte Export**: PDF/Excel pentru comenzi și inventar
- [ ] **Multi-location**: Suport pentru multiple cafenele
- [ ] **Programe de Loialitate**: Puncte și reduceri pentru clienți fideli
- [ ] **API REST**: Endpoint-uri pentru aplicații mobile
- [ ] **Dashboard Analitic Avansat**: Grafice interactive cu Chart.js
- [ ] **Sistem de Rezervări**: Rezervări mese online
- [ ] **Integrare POS**: Conectare cu terminale de vânzare fizice
- [ ] **Multi-language**: Suport pentru mai multe limbi

## 🤝 Contribuții

Contribuțiile sunt binevenite! Dacă dorești să contribui:

1. Fork repository-ul
2. Creează un branch pentru feature-ul tău (`git checkout -b feature/AmazingFeature`)
3. Commit modificările (`git commit -m 'Add some AmazingFeature'`)
4. Push pe branch (`git push origin feature/AmazingFeature`)
5. Deschide un Pull Request

### Ghid de Contribuție

- Respectă stilul de cod existent
- Adaugă docstrings pentru funcții noi
- Testează toate modificările înainte de commit
- Actualizează documentația când este necesar

## 📝 Licență

Acest proiect este licențiat sub MIT License - vezi fișierul [LICENSE](LICENSE) pentru detalii.

## 👤 Autor

**Numele Tău**
- GitHub: [@username](https://github.com/username)
- LinkedIn: [Numele Tău](https://linkedin.com/in/username)
- Email: email@example.com

## 🙏 Mulțumiri

- Django Documentation pentru resurse excelente
- Comunitatea Python pentru suport
- Toți cei care au testat și oferit feedback

---

**Dezvoltat cu ❤️ și ☕ în România**

*Pentru suport sau întrebări, deschide un issue pe GitHub.*