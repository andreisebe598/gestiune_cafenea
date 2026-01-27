# ☕ Coffee Management System (Django)

Sistem robust de gestiune pentru cafenele, axat pe automatizarea inventarului și procesarea eficientă a comenzilor. Proiectul demonstrează utilizarea avansată a framework-ului Django și a conceptelor de arhitectură software.

## 🚀 Key Technical Highlights (Pentru CV)

* **🛒 Logică de Coș Complexă (`cart.py`):** Implementarea unui sistem de management al cumpărăturilor bazat pe sesiuni, permițând manipularea datelor fără a aglomera baza de date prematur.
* **⚡ Automatizare prin Django Signals (`signals.py`):** Am implementat un mecanism de tip "Observer" care actualizează automat stocurile de ingrediente în timp real imediat ce o comandă este confirmată.
* **🏗️ Arhitectură Modulară:** Separarea clară între logica de business (Modele), interfața de administrare și partea de user-facing templates.
* **🔐 Securitate:** Gestionarea variabilelor de mediu prin `.env` pentru protejarea cheilor secrete și a datelor bazei de date.

## 🛠️ Stack Tehnologic
* **Backend:** Python 3.x, Django 4.x
* **Frontend:** Django Templates, CSS3, JavaScript
* **Tooling:** Pip, Virtualenv, Git

## 📦 Instalare și Rulare
1. Clonează repo-ul: `git clone [link-ul-tau]`
2. Creează venv: `python -m venv venv`
3. Activează venv: `Scripts\activate`
4. Instalează dependențele: `pip install -r requirements.txt`
5. Migrează baza de date: `python manage.py migrate`
6. Start: `python manage.py runserver`