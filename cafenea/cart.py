# The `Cart` class manages a shopping cart for a Django web application, allowing users to add,
# remove, and view products with their quantities and prices.
from decimal import Decimal
from django.conf import settings
from .models import Produs

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart_session_id')

        if not cart:
            cart = self.session['cart_session_id'] = {}
        self.cart = cart

    def add(self, produs_id, cantitate=1, update_quantity=False):
        produs_id=str(produs_id)

        if produs_id not in self.cart:
            self.cart[produs_id] = {'cantitate': 0, 'pret': str(0)}

        if update_quantity:
            self.cart[produs_id]['cantitate'] = cantitate
        else:
            self.cart[produs_id]['cantitate'] += cantitate
            
        self.save()

    def remove(self, produs_id):
        produs_id = str(produs_id)
        if produs_id in self.cart:
            del self.cart[produs_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Produs.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['product'].pret_vanzare)
            item['total_price'] = item['price'] * item['cantitate']
            yield item

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self:
             total += item['total_price']
        return total

    def __len__(self):
        return sum(item['cantitate'] for item in self.cart.values())

    def clear(self):
        del self.session['cart_session_id']
        self.save()

    def save(self):
        self.session.modified = True