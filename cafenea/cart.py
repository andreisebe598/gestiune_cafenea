"""
Clasa ce implementeaza logica cosului de cumparaturi ce persista pe durata sesiunii utilizatorului. Nu foloseste un model de vaza de date pentru stocarea cosului, 
utilizeaza in schimb 'request.session' din Django

Aspecte Cheie:
1. **Stocare in sesiune:** - Cosul este stocat in 'request.session' sub cheia 'cart_session_id', permiand persistenta intre request-uri pentru utilizatorul curent
2. **Interfata simpla:** - Metodele 'add', 'remove', 'clear' ofera o interfata intuitiva pentru manipularea continutului cosului
3. **Calcul automat al totalului:** - Metoda 'get_total_price' face calculul total al produselor din cos la cerere
4. **Iterare prin produse:** - Metoda '__iter__' permite parcurgerea elementelor din cos si asocierea lor cu obiectele reale de tip 'Produs'
5. **Actualizare sesiune:** - Metoda 'save' asigura salvarea modificarilor in sesiune:** -
"""
from decimal import Decimal
from django.conf import settings
from .models import Produs

class Cart(object):
    def __init__(self, request):
        
        """
        Initializeaza cosul de cumparaturi si verifica daca exista sau nu un cos in sesiunea utilizatorului. Daca nu exista se creaza unul gol
        """

        self.session = request.session
        cart = self.session.get('cart_session_id')

        if not cart:
            cart = self.session['cart_session_id'] = {}
        self.cart = cart

    def add(self, produs_id, cantitate=1, update_quantity=False):

        """
        Adauga un produs in cos sau actualizeaza cantitatea acestuia

        Argumente:
            produs_id: Id-ul produsului din paza de date
            cantitate (int): Cantitatea de adaugat in cos
            update_quantity (bool): Daca este True, cantitatea este inlocuita. Daca este False, cantitatea este incrementata
        """

        produs_id=str(produs_id) #Convertire la string. Cheile JSON trebuie sa fie string-uri

        if produs_id not in self.cart:
            self.cart[produs_id] = {'cantitate': 0, 'pret': str(0)}

        if update_quantity:
            self.cart[produs_id]['cantitate'] = cantitate
        else:
            self.cart[produs_id]['cantitate'] += cantitate
            
        self.save()

    def remove(self, produs_id):

        """
        Elimina complet un produs din cos in functie de id
        """

        produs_id = str(produs_id)
        if produs_id in self.cart:
            del self.cart[produs_id]
            self.save()

    def __iter__(self):

        """
        Generator care itereaza prin elementele din cos. Acesta preia obiectele 'Produs' din baza de date in functie de ID-urile din sesiune

        Returneaza:
            Un dictionar pentru fiecare produs ce contine:
                - produs (obiect model), pret, cantitate, total_price
        """

        product_ids = self.cart.keys()
        #Interogare optimizata: selecteaza toate produsele deodata
        products = Produs.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            #convertim pretul din string/floar in Decimal pentru calcule
            item['price'] = Decimal(item['product'].pret_vanzare)
            item['total_price'] = item['price'] * item['cantitate']
            yield item

    def get_total_price(self):
        """
        Calculeaza pretul total al produselor din cos
        """
        total = Decimal('0.00')
        for item in self:
             total += item['total_price']
        return total

    def __len__(self):
        #Returneaza numarul total de produse din cos
        return sum(item['cantitate'] for item in self.cart.values())

    def clear(self):
        #Goleste cosul ( metoda apelata deobicei la finalizarea comenzii )
        del self.session['cart_session_id']
        self.save()

    def save(self):
        #Marcheaza sesiunea ca fiind modificata pentru a asigura salvarea datelor in DB
        self.session.modified = True