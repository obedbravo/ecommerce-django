from django.db import models
from store.models import Product, Variation #se imporat el modelo producto
from accounts.models import Account
# Create your models here.

class Cart(models.Model): #carrito contador
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):  #productos del carrito de compras agregado
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True) #SE AÑADIO OTRO CAMPO DE COLLECION PARA LOS VARIANTES TALLA Y  COLOR
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity



    def __unicode__(self):
        return self.product

