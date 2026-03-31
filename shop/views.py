from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product
from cart.forms import CartAddProductForm
from myshop.translit import *
import csv
#import re

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all().filter(parent_id=None)
    #products = Product.objects.all().filter(available=True)[:30]
    cats = None #categories
    q = request.GET
    search = q.get('search','').strip().upper()
    #print(search)
    if len(search)>2:	#Поиск по полю search
      if search.isdigit():
        if len(search) > 10:  #barcode
          products = Product.objects.all().filter(barcode = f'{search}')
        else:
          products = Product.objects.all().filter(incode = f'{search}')
      else:
        products = Product.objects.all().filter(Q(name__startswith=search) | Q(name__icontains=search),available=True)
    elif category_slug:
        category = get_object_or_404(Category,
            slug=category_slug)
        cats = Category.objects.all().filter(parent_id=category)
        products = Product.objects.all().filter(category=category)
    else:
        products = Product.objects.all().filter(available=True).filter(rest__gt=0)    

    paginator = Paginator(products,9)
    page_number = q.get('page',1)
    prlist = paginator.page(page_number)
    #cart_product_form_list = CartAddProductFormList()
    return render(request,
        'shop/product/list.html',
        {'category': category,
        'categories': categories,
        'products': prlist,
		'cats':cats,
        'search':search})

# Create your views here.
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
        id=id,
        slug=slug,
        available=True)
    cart_product_form = CartAddProductForm()        
    return render(request,
        'shop/product/detail.html',
        {'product': product,
        'cart_product_form': cart_product_form})

def search (request,search):
	print(search)
	
        

def import_categ(request,fcateg):
	fcat = fcateg
	if fcat.find('group') > -1:
		print(fcateg)   
		ndel = Category.objects.all().delete()
		finp = open(fcat,encoding='cp1251')
		categlist = csv.reader(finp,delimiter=';')
		catsort = list(categlist)[1:]
		catsort.sort(key=lambda x: int(x[3],36) * 10000000 + int(x[0],36))
		cobj = []
		'''for cat in catsort:
				cobj=Category(pk=int(cat[0],36),name=cat[2],slug=slugify(cat[2]+cat[0]))
				cobj.save()
		'''
		for cat in catsort:
			cobj.append(Category(pk=int(cat[0],36),name=cat[2],slug=slugify(cat[2]+cat[0])))
		catobjects=Category.objects.bulk_create(cobj,100)
		for cat in catsort:
			if cat[3] > '0':
				pn = Category.objects.get(pk=int(cat[3],36))
				cobj=Category.objects.get(pk=int(cat[0],36))
				cobj.parent_id=pn
				cobj.save()
		return HttpResponse(f'<h3>Обработано {len(catsort)} записей </h3>')
	elif fcat.find('price') > -1:
		fpr = open(fcat,encoding='cp1251')
		pcsv = csv.reader(fpr, delimiter=';')
		ndel = Product.objects.all().delete()
		#ndel = 0
		cats = Category.objects.all()
		cnt = 0
		prd = []
		for rw in pcsv:
			if cnt > 0:
				try:
					parent_cat = cats.get(id=int(rw[0],36))
					prd.append( Product(id=int(rw[1]),category=parent_cat, incode=rw[1],name = rw[2],slug = slugify(rw[2]),
						barcode=rw[4],articul=rw[3],description='',rest=int(rw[5]),prop=rw[6],upak=rw[7],
						price=float(rw[10]),cena=rw[8],cenof=rw[9],cenoc=rw[10]))
					#prd.save()
				except:
					print(rw)
			cnt += 1
			#if cnt % 100 == 0:
			#	print (f'Price pos {cnt}')	
		ppobj = Product.objects.bulk_create(prd,400)
		return HttpResponse(f'<h3>Прайс: удалено {ndel} поз., обработано {cnt} позиций</h3>')
	pass


