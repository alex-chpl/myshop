from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self',null=True,blank=True,related_name='category',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
        unique=True)
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
        args=[self.slug])
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,
        related_name='products',
        on_delete=models.CASCADE)
    incode = models.CharField(max_length=10, default='',unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    #image = models.ImageField(upload_to='image',
    #    blank=True)
    barcode =  models.CharField(max_length=24,blank=True,null=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    articul = models.CharField(max_length=100,blank=True,null=True)
    rest = models.IntegerField(default = 0)
    upak = models.CharField(max_length=100,blank=True,null=True)
    prop = models.CharField(max_length=100,blank=True,null=True)
    cena = models.CharField(max_length=15,default="0.0") #rozn
    cenof = models.CharField(max_length=15,default="0.0") #optf
    cenoc = models.CharField(max_length=15,default="0.0") #optch

    @property
    def price_rub(self):
        return str(float(self.price * 1))

    def get_absolute_url(self):
        return reverse('shop:product_detail',
            args=[self.id, self.slug])
    @property
    def get_image(self):
        return 'https://divo-m.ru/image/'+str(self.barcode)+'.jpg'


    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['incode']),
            models.Index(fields=['barcode']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

