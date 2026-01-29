'''
Acest modul automatizeaza sincronizarea dintre modelul standard de autentificare ('User') si modelul din baza de date ('Client'). Utilizeaza semnalul 'post_save' pentru a declansa
niste actiuni de save/update automate la crearea sau actualizare utilizatorilor

Aspecte Cheie:
1. **Legatura 1-la-1 dintre User Si client:** - Asigura ca pentru fiecare User creat, exista un obiect Client asociat
2. **Logica de naming pentru erori:** - Construieste automat numele complet folosind last_name si first_name, iar in cazul in care nu exista este folosit automat username-ul.
3. **Mecanism de Self-Healing:** - Functia save_client_profile' actioneaza ca un sistem de siguranta. Daca dintr-o eroare anterioara sau o migrare manuala un User ramane fara un Client
asociat acesta va fi creat automat la urmatoarea salvare
4. **Setare automata a genului:** - seteaza gen = "Nespecificat" ca valoare default
'''

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Client

@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    '''
    Creaza un obiect Client imediat ce un User este inserat in baza de date
    '''
    if created:
        nume_complet = f"{instance.last_name} {instance.first_name}".strip()
        
        if not nume_complet:
            nume_complet = instance.username

        Client.objects.create(
            user=instance,
            nume=nume_complet,
            gen='Nespecificat' 
        )

@receiver(post_save, sender=User)
def save_client_profile(sender, instance, **kwargs):
    '''
    Asigura persistenta profilului de Client la modifcarea User-ului si creeaza profilul daca acesta lipseste ( un User mai vechi sau inserarea manuala a unui User )
    '''
    try:
        instance.client.save()
    except Client.DoesNotExist:
        nume_complet = f"{instance.last_name} {instance.first_name}".strip() or instance.username
        Client.objects.create(user=instance, nume=nume_complet)