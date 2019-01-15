from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string
from django.db.models.signals import post_save
from django.urls import reverse

def GeneratedCode():
  l = []
  for u,_ in enumerate(range(10)):
    if u == 0 or u == 3 or u == 6 or u == 7 or u == 9:
      l.append(string.ascii_lowercase[random.randint(0, 25)])
    else:
      l.append(str(random.randint(1, 9)))

  return ''.join(l)

def GeneratedApiCode():
  l = []
  for u,_ in enumerate(range(25)):
    if u % 2 != 0 or u == 4 or u == 8 or u == 12 or u == 14:
      l.append(string.ascii_lowercase[random.randint(0, 25)])
    else:
      l.append(str(random.randint(1, 9)))

  return ''.join(l)

class Transaction(models.Model):
    methods = (('cash', 'cash'),('credit','credit'),('check','check'))
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    payment_method = models.CharField(max_length=10, choices=methods, default='cash')
    last_4 = models.PositiveIntegerField(null=True)
    returned = models.BooleanField(default=False)
    items = models.ForeignKey('Item', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    cashier = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)

    def validation_last_4(self, value):
      if self.method == 'credit':
          if self.last_4 == None or self.last_4 < 999:
              raise ValidationError('method was credit, but last_4 digits werent given')

class Returned(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    refund_price = models.PositiveIntegerField()
    items_returned = models.ManyToManyField('ReturnTag')
    confirmed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    type_of_weight = (('lb','lb'),('oz','oz'))
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category =  models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(null=True)
    on_sale = models.BooleanField(default=False)
    sale = models.ForeignKey('On_Sale', on_delete=models.CASCADE, null=True)
    item_serial_id = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    purchased = models.PositiveIntegerField(default=0)
    returned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + ' - ' + self.price

    def get_absolute_url(self):
        return reverse('product:dItem', kwargs={'uuid':self.uuid})

class On_Sale(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_active_date = models.DateField()
    last_active_date = models.DateField()
    store = models.ForeignKey('Store', on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=255)
    return_policy = models.ForeignKey('ReturnPolicy', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    def __str__(self):
        return self.name + ' - ' + self.store.name

    def get_absolute_url(self):
        return reverse('product:rCategory', kwargs={'uuid':self.uuid})

class ReturnPolicy(models.Model):
    elapse_days = models.PositiveIntegerField()
    holiday_elapse_days = models.PositiveIntegerField()
    #name = models.CharField(max_length=100)
    apply_to_sales = models.BooleanField(default=True)
    store = models.OneToOneField('Store')
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.store.name + 'return policy'

    def get_absolute_url(self):
        return reverse('product:rReturnPolicy', kwargs={'uuid':self.uuid})

class PrintTagItems(models.Model):
    Req = (('total price','total price'),('item price','item price'),('category','category'),('select','select'),('all','all'),)
    requirements = models.CharField(max_length=20, choices=Req)
    price = models.PositiveIntegerField(null=True)
    items = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    store = models.OneToOneField('Store')
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.store.name + 'Print Tag Rules'

    def get_absolute_url(self):
        return reverse('product:rPItem', kwargs={'uuid':self.uuid})

class PurchaseTag(models.Model):
    lookup_code = models.CharField(max_length=10, default=GeneratedCode(), editable=False)
    created = models.DateTimeField(auto_now_add=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    returned = models.BooleanField(default=False)
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

#one for every item being returned
class ReturnTag(models.Model):
    verified = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    c_score = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    employee_processing_return = models.ManyToManyField('Employee', blank=True)
    lookup_code = models.CharField(max_length=10, default=GeneratedCode(), editable=False)
    purchase_tag = models.OneToOneField(PurchaseTag)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)

    #this the tag that gets printed when verifed by by ars, then the employee verified it by using the lookup code to change to verifed


class ParentStore(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    state = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
    users =  models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

class Store(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    state = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
    #parent_store = models.ForeignKey(ParentStore, on_delete=models.CASCADE, null=True)
    min_c_score = models.PositiveIntegerField(default=70)
    api_code = models.CharField(max_length=25, default=GeneratedApiCode(), editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user =  models.OneToOneField(User)

    def __str__(self):
        return self.name


class Employee(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    employee_name = models.CharField(max_length=255)
    employee_identifier = models.CharField(max_length=255, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


def CreateStoreByUser(sender, **kwargs):
    if kwargs['created']:
        Store.objects.create(user=kwargs['instance'])

post_save.connect(CreateStoreByUser, sender=User)
