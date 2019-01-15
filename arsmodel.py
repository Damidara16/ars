from django.models import model
from django.core.exceptions import ValidationError

class Transaction(models.Model):
  methods = (('cash', 'cash'),('credit','credit'),('check','check'))
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  payment_method = models.CharField(max_length=10, choices=methods, default='cash')
  last_4 = models.PositiveIntegerField(null=True, validators=[validation_last_4])
  items = models.ForeignKey(Item, on_delete=models.CASCADE)
  store = models.ForeignKey(Store, on_delete=models.CASCADE)
  cashier = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
  total = models.PositiveIntegerField()

  def validation_last_4(self):
      if self.method == 'credit':
          if self.last_4 == None or self.last_4 == null:
              raise ValidationError('method was credit, but last_4 digits werent given')


class Category(models.Model):
    name = models.CharField(max_length=255)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    ReturnPolicy

class ReturnPolicy(models.Model):
    elapse_days
    holiday_elapse_days
    name
    apply_to_sales

class PrintTagItems(models.Model):
    Req = (('total price','total price'),('item price','item price'),('category','category'),('select','select'),('all','all'),)
    requirements = models.CharField(max_length=20, choices=Req)
    price = models.PositiveIntegerField(null=True)
    items = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    store = models.OneToOneField(Store)


class ReturnTag(models.Model):
  date = models.DateTimeField(auto_add_now=True)
  method_of_payment = models.ManyToMany()
  store = models.ManyToMany(Store)
  item = models.ManyToMany(Item)
  cashier = models.ManyToMany(Employee)
  returned = models.BooleanField(default=False)
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())

#one for every item being returned
class Returned_C_Score_Result(models.Model):
  store_of_return = models.ManyToMany()
  verified = models.Boolean(default=False)
  failed = models.Boolean(default=False)
  c_score = models.PositiveIntergerField(default=0)
  date = models.DateTimeField(auto_add_now=True)
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  employee_processing_return = models.ManyToMany(Employee, blank=True)
  itemReturnTag = models.OneToOne(ReturnTag)
  lookup_code = models.CharField(max_length=255)

  """
  TO VERIFY RETURN, EMPLOYEE WILL ENTER IN LOOKUP_CODE, ALONG WITH THE TAG ID, AND THAT DATA WILL BE SENT TO A VIEW
  WHICH WILL MATCH THE TAG ID AND RETURN ID AND THEN CHANGE THE RETURN MODEL FIELD TO VERIFIED. AND CHANGE THE TAGS
  SO THAT THEY CAN NOT BE REUSED AGAIN.
  """
  def save(self, *args, **kwargs):
      if self.c_score < 80:
          self.failed = True
      self.lookup_code = loopupCreate()
          return super(Returned_C_Score_Result).save(*args, **kwargs)

class Returned(models.Model):
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  refund_price = models.PositiveIntergerField()
  items_returned = models.ManyToMany(Returned_C_Score_Result)
  confirmed = models.BooleanField(default=False)
  date = models.DateTimeField(auto_add_now=True)

class Item(models.Model):
  Categories = (())
  type_of_weight = (('lb','lb'),('oz','oz'))
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  category = models.Charfield(max_length=255, choices=Categories)
  name = models.Charfield(max_length=255)
  price = models.PositiveIntergerField(null=True)
  on_sale = models.BooleanField(default=False, null=True)
  item_serial_id = models.CharField(max_length=255)
  weight = models.DecimalField()

class On_Sale(models.Model):
    first_active_date =
    last_active_date =
    item =
"""class ParentStore(models.Model):
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  state = models.Charfield(max_length=255)
  name = models.Charfield(max_length=255)
  street = models.Charfield(max_length=255)
  street2 = models.Charfield(max_length=255)
  phone_number = models.Charfield(max_length=10)
  zip_code = models.Charfield(max_length=10)
"""
class Store(models.Model):
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  state = models.Charfield(max_length=255)
  name = models.Charfield(max_length=255)
  street = models.Charfield(max_length=255)
  street2 = models.Charfield(max_length=255)
  phone_number = models.Charfield(max_length=10)
  zip_code = models.Charfield(max_length=10)
  parent_store = models.ForeignKey(ParentStore, on_delete=models.CASCADE)
  categories = models.ForeignKey(Category, on_delete=models.CASCADE)

class Employee(models.Model):
  uuid = models.UUIDField(primarykey=True, editable=False, default=uuid.uuid())
  employee_name = models.CharField(max_length=255)
  employee_identifier = models.CharField(max_length=255, null=True)



"""
views

lookup -> Returned, ReturnTag, ReturnRequest
save -> all models
edit -> ReturnTag, Item
"""
