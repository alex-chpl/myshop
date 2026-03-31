from shop.models import *
import csv
import os,sys

def updt_categ(categ):
  for cat in categ:
    cobj = Category(id=cat[0],parent=cat[1],name=cat[2])
    cobj.save()

if __name__ == '__main__':
    fcat = open(sys.argv[1],encoding='cp1251')
    ct = csv.reader(fcat,delimiter=';')
    clist = [[int(e[3],36),int(e[0],36),e[2]] for e in ct[1:]]
    updt_categ(clist)
