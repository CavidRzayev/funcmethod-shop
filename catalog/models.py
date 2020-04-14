from django.db import models
from django.utils.text import slugify
from time import time
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from PIL import Image
import os
import glob
#from simple_history.models import HistoricalRecords

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'brand_slug': self.slug})

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+str(self.name))
        super(Brand, self).save(*args, **kwargs)
    
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

class Category(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Brand')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    img = models.ImageField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+str(self.name))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)

    return new_slug + '_' + str(int(time()))


class Color(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    


class Product(models.Model):
    category = models.ForeignKey(SubCategory,on_delete=models.CASCADE, verbose_name='Kategoriya')
    colors = models.ForeignKey(Color,on_delete=models.CASCADE, verbose_name='Rengi', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Brand')
    name = models.CharField(max_length=1000, verbose_name='Mehsulun Adi')
    code = models.CharField(max_length=100, verbose_name='Mehsulun Kodu')
    image = models.ImageField()
    price = models.DecimalField(max_digits=9, decimal_places=0, default=0, verbose_name='Qiymeti')
    sale = models.DecimalField(max_digits=9, decimal_places=0, default=0,  verbose_name='Endirim Faizi', blank=True, null=True)
    dicount = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Yekun Qiymeti', blank=True, null=True)
    order_price = models.DecimalField(max_digits=9, decimal_places=2,  verbose_name='Catdirilma Qiymeti', blank=True, null=True)

    title = models.TextField()
    description = models.TextField()
    
    data = models.DateField(auto_now_add=True)
    stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    promo_kod = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    material = models.CharField(max_length=200, blank=True, verbose_name='Material')
    olcu = models.CharField(max_length=200, blank=True, verbose_name='Olculer')
    #history = HistoricalRecords()
    #fovarite = models.BooleanField(default=False)


    def save (self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        if not self.dicount:
            self.dicount = self.price - (self.price * self.sale / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}' + ' , "' + f'{self.data}" '

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})

class MultiImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Image')
    
class CartItem(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def  __str__(self):
        return "Cart item for product {0}".format(self.product.title)


class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def  __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        cart_items = [item.product for item in cart.items.all()]
        if new_item.product not in cart_items:
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

ORDER_STATUS_CHOICES = (
	('Qeyde alindi', 'Qeyde alindi'),
	('Icra olunur', 'Icra olunur'),
	('Odenilib', 'Odenilib')
)

class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey('Cart', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=40, choices=(('Magazada', 'Magazada'), 
        ('Catdirilma', 'Catdirilma')), default='Magazada')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def  __str__(self):
        return "Muraciyet №{0}".format(str(self.id))


class Fovarite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fovarit = models.ManyToManyField(Product, blank=True, related_name='fovar')

  
    