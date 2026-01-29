'''
Acest fisier defineste clasa de configurare pentru aplicatia 'cafenea' si este punctul de intrare pentru setarile specifice acestei aplicatii in cadrul proiectului

Aspecte Cheie:
1. **Initializare la pornire:** - Metoda 'ready' este executata o singura data imediat ce Django a incarcat setarile si a initializat registrii de modele
2. **Activarea semnalelor (Signals):** - Cel mai important rol al fisierului este importarea codului din 'signals.py'. Fara linia din metoda 'ready', semnalele 'post_save'
nu ar fi activate si automatismele descrise in signals.py nu ar functiona
3. **Configurare DB:** - 'default_auto_field' specifica tipul de camp autoincremental folosit pentru ID-urile modelelor
'''

from django.apps import AppConfig

class CafeneaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafenea'

    def ready(self):
        """
        Importa semnalele aplicatiei la initializare pentru a le activa
        """
        import cafenea.signals  # type: ignore