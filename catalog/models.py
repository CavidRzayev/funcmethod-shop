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
#from PIL import Image
import os
import glob
from django.conf import settings
from star_ratings.models import Rating
from io import BytesIO
#from PIL import Image
from django.core.files import File
from ckeditor.fields import RichTextField
from colorful.fields import RGBColorField
from sortedm2m.fields import SortedManyToManyField

#from simple_history.models import HistoricalRecords
import math
from django.contrib.auth.models import (
  AbstractBaseUser,
  BaseUserManager
)
# Create your models here.
def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=90) 
    new_image = File(im_io, name=image.name)
    return new_image

def gen_random_promo():
    #new_slug = slugify(s, allow_unicode=True)

    return str(int(time()))


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)

    return new_slug + '_' + str(int(time()))


class Banner(models.Model):
      image = models.ImageField()
      link = models.CharField(max_length=50)

      def __str__(self):
          return self.link
      
   



class ProductQuerySet(models.query.QuerySet):


    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__search=query) | 
                   Q(name__search=query) | 
                   Q(slug__icontains=slugify(query)) |
                   Q(category_name__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
  def get_queryset(self):
    return ProductQuerySet(self.model, using=self._db)
  
  def all(self):
    return self.get_queryset().active()
  
  def featured(self):
    return self.get_queryset().featured()

  def get_by_id(self, id):
    qs = self.get_queryset().filter(id=id)
    if qs.count() == 1:
      return qs.first()
    return None

  def search(self, query):
    return self.get_queryset().active().search(query)




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
    
class MainCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
      return self.name
    

class Category(models.Model):
    maincategory = models.ForeignKey(MainCategory, blank=True, null=True, on_delete=models.CASCADE, related_name='post')
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    

    #def save(self, *args, **kwargs):
     #   self.slug = slugify(self.name)
      #  super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})




class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='sub')
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.name



    #def save (self, *args, **kwargs):
     # if not self.slug:
      #  self.slug = gen_slug(self.name) 
      #super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subcategory_detail', kwargs={'subcategory_slug': self.slug})
    


class Product(models.Model):
    category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True, null=True ,related_name='pro', verbose_name='Kategoriya')
    category_name = models.CharField(max_length=1000, verbose_name='Mehsulun categoriyasi',blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Brand',blank=True, null=True)
    name = models.CharField(max_length=1000, verbose_name='Mehsulun Adi')
    code = models.CharField(max_length=100, verbose_name='Mehsulun Kodu',blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    barcode = models.CharField(max_length=100, verbose_name='Bar kod')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Qiymeti')
    sale = models.DecimalField(max_digits=9, decimal_places=0, default=0,  verbose_name='Endirim Faizi', blank=True, null=True)
    dicount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Yekun Qiymeti', blank=True, null=True)
    order_price = models.DecimalField(max_digits=9, decimal_places=2,  verbose_name='Catdirilma Qiymeti', blank=True, null=True)
    reting = models.IntegerField(verbose_name='Reyting', blank=True, null=True)
    title = RichTextField()
    main_color = RGBColorField(blank=True, null=True)
    #description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    data = models.DateField(auto_now_add=True)
    stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    month_6 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, verbose_name='Kredit 6 ay ucun ayliq odenis')
    month_9 =models.DecimalField(max_digits=9, decimal_places=2, blank=True, verbose_name='Kredit 9 ay ucun ayliq odenis')
    month_12 =models.DecimalField(max_digits=9, decimal_places=2, blank=True, verbose_name='Kredit 12 ay ucun ayliq odenis')
    month_15 =models.DecimalField(max_digits=9, decimal_places=2, blank=True, verbose_name='Kredit 15 ay ucun ayliq odenis')
    month_18 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, verbose_name='Kredit 18 ay ucun ayliq odenis')
    #promo_kod = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    material = models.CharField(max_length=200, blank=True, verbose_name='Material')
    
    objects = ProductManager()

    def prome_code_in(self):
       return self.codes.all().count()

    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        #if not self.dicount:
         #   self.dicount = self.price - (self.price * self.sale / 100)
        iyirmi = self.price * 20 / 100
        print(iyirmi)
        ilkin = float(self.price) - float(iyirmi)
        print(ilkin)
        if not self.month_6:
            
            self.month_6 = float(self.price) - float(ilkin)
            self.month_6 = ilkin  / 6 
        if not self.month_9:
            self.month_9 = self.price + (self.price * 10 / 100)
            self.month_9 = ilkin  / 9 
        if not self.month_12:
            self.month_12 = self.price + (self.price * 10 / 100)
            self.month_12 = ilkin  / 12
        if not self.month_15:
            self.month_15 = self.price + (self.price * 10 / 100)
            self.month_15 = ilkin  / 15  
        if not self.month_18:
            self.month_18 = self.price + (self.price * 10 / 100)
            self.month_18 = ilkin  / 18 
       
       
       # new_image = compress(self.image)
        #self.image = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}' + ' , "' + f'{self.data}" '

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="color")
    color = RGBColorField(blank=True, null=True)
    color_name = models.CharField(max_length=100,blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True,null=True)
    
    
    def __str__(self):
        return self.color_name
   


    def get_absolute_url(self):
        return reverse('color_detail', kwargs={'color_slug': self.id})



class MultiImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Image', blank=True, null=True)
    
    
    #def save(self, *args, **kwargs):
     # new_image = compress(self.image)
      #self.image = new_image
      #super().save(*args, **kwargs)

    
class CartItem(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    color = models.CharField(max_length=100, blank=True, null=True)
    def  __str__(self):
        return "{0} , rengi - {1}".format(self.product.name, self.color)

class CompanyPromoCode(models.Model):
    name = models.CharField(max_length=400, verbose_name='Kampaniya Adi')
    faiz = models.IntegerField(default=0,blank=True, null=True,verbose_name='Endirim Faiz Derecesi')
    #products = models.ManyToManyField(Product, verbose_name='Mehsullar', related_name='company')
    code = models.CharField(max_length=300, verbose_name='Code')
    money = models.CharField(max_length=300, default=0, blank=True, null=True, verbose_name='Manat')
    limit = models.IntegerField(default=0, verbose_name='Maksimum istifade Dayi - Limit ( +1 yazilmalidi)')
    count = models.IntegerField(default=0,verbose_name='Promocoddan istifade olunub', blank=True, null=True)
    def __str__(self):
        return self.name

    

    
    
class Size(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Olculer',blank=True, null=True)

    def __str__(self):
        return self.name
    

class PromoCode(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='codes')
    name = models.IntegerField(verbose_name='Promocodun Faiz Derecesi',blank=True, null=True)
    code = models.CharField(max_length=300, verbose_name='Code', blank=True)
    def save (self, *args, **kwargs):
       
        if not self.code:
            #x = self.product.price + (self.product.price * self.faiz / 100 )
            self.code = gen_random_promo()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.product.name

class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    color = models.CharField(max_length=100, blank=True, null=True)

    def  __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug, color, qty):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.dicount, color=color, qty=qty)
       
        cart_items = [item.product for item in cart.items.all()]
        if new_item.product not in cart_items:
            cart.items.add(new_item)
            try:
              cart.color(color)
            except:
              pass
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
        if cart_item.product.sale > 0:
            cart_item.item_total = int(qty) * Decimal(cart_item.product.dicount)
        else:
            cart_item.item_total = int(qty) * Decimal(cart_item.product.dicount)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

ORDER_STATUS_CHOICES = (
  ('0', 'Icra olunmayib'),
	('1', 'Yoldadir'),
	('2', 'Çatdırılıb'),
	('3', 'Imtina edilib'),
  ('4', 'Qaytarilib')
)

class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='item')
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


#lass Fovarite(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   # fovarit = models.ManyToManyField(Product, blank=True, related_name='fovar')

  
    
class Click(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
  def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
    if not email:
      raise ValueError('Users must have an email address')
    if not password:
      raise ValueError('Users must have a password')
    

    user_obj = self.model(
      email=self.normalize_email(email),
    )
    user_obj.set_password(password)
    user_obj.staff = is_staff
    user_obj.admin = is_admin
    user_obj.is_active = is_active
    user_obj.save(using=self._db)
    return user_obj

  def create_staffuser(self, email,  password):
    user = self.create_user(
      email,
      password=password,
      is_staff=True
    )
    user.staff = True
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password):
    user = self.create_user(
      email,
      password=password,
      is_staff=True,
      is_admin=True
    )
    user.staff = True
    user.admin = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser):
  email = models.EmailField(max_length=255, unique=True)
  last_name = models.CharField(max_length=100, blank=True)
  phone = models.IntegerField(blank=True, null=True)
  brity = models.DateField(blank=True, null=True)
  username = models.CharField(max_length=100, blank=True)
  first_name = models.CharField(max_length=100, blank=True)
  #full_name = models.CharField(max_length=255, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  staff = models.BooleanField(default=False)
  admin = models.BooleanField(default=False)
  timestamp = models.DateTimeField(auto_now_add=True)

  USERNAME_FIELD = 'email'

  #REQUIRED_FIELDS = ['email']
  
  objects = UserManager()

  def __str__(self):
    return self.email

  def get_username(self):
    if not self.username:
        x = self.username = self.email
        return x
    #return self.email

  def get_short_name(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    if self.is_admin:
      return True
    return self.staff

  @property
  def is_admin(self):
    return self.admin


from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator


class Tag(models.Model):
  title = models.CharField(max_length=120)
  slug = models.SlugField(blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)
  products = models.ManyToManyField(Product, blank=True)

  def __str__(self):
    return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)


class HistoryProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    #date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.product.name
    
class Comment(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
  text = models.TextField()
  date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  
  class Meta:
    ordering = ['-date']

  def __str__(self):
      return self.product.name
  
class Phone(models.Model):
  phone = models.CharField(max_length=100)
  def __str__(self):
    return self.phone


class Message(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senders")
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=300, verbose_name='Basliq')
  message = models.TextField(verbose_name='Mesaj')
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.user.email

class LandingPage(models.Model):
  title = RichTextField()
  slug = models.SlugField(max_length=500 ,blank=True)
  category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True, null=True ,related_name='landing', verbose_name='Kategoriya')
  products = models.ManyToManyField(Product,related_name='pr',blank=True)

  def __str__(self):
      return self.slug
  
