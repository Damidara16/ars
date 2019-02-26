from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from product.models import *
from .forms import *
from django.urls import reverse
from django.http import Http404

"""
can be called direct by using our api library or by webhooks calling our api directly

ex.
ars.PurchaseTag.create(...)
"""
def Home(request):
    if request.user.is_authenticated():
        return render(request, 'product/home.html')
    else:
        return render(request, 'product/unauthHome.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('product:home'))

        else:
            #messages.error(request, "Error")
            return render(request, 'product/create.html', {'form':form})

    else:
        form = RegistrationForm()
        return render(request, 'product/create.html', {'form':form})


"""

method of payment
date of purchase
item condition
elapse days
store of purchase origin
2 deterent questions
weight
size - sm or md or large
category
name of item
item price
was item on sale

"""
#c-score is called per each item, all questions are multiple choice
#for untagged ask few question to see if item requires tag
def CreateC_ScoreUnTagged(request):
    pass

def CreateC_Score(request):
    pass
    #serializer = CSerializer(data=request.data):
    #if serializer.is_valid():

def collectItems(items, user, uuid):
    l = []
    t = Transaction.objects.get(uuid=uuid)
    for i in items:
        a = PurchaseTag.objects.create(store=user, transaction=t, item=i)
        l.append(a.uuid)
        return l
#list of uuids, the library func will then recall django will the uuids to print the tags
#CAN PRINT TAG BASED OF TOTAL TRANSACTION AMOUNT AND PRINT A TAG FOR EACH ITEM
#CAN PRINT TAG BASED ON INDIVIUAL ITEM PRICE
#CAN PRINT TAG BASED CATEGORY OF ITEM
#CAN PRINT TAG BASED ON CERTAIN ITEMS

#could use ip to decide which store it is or the store passes it themselves
def LogTransaction(request):

    serializer = LogSerializer(data=request.data)
    if serializer.is_valid():
        store = request.user.store
        requirements = store.PrintTagItems.requirements
        serializer.save()
        if requirements == 'item price':
            m = []
            for i in serializer.data['items']:
                if i.price > store.PrintTagItems.price:
                    m.append(i)
            a = collectItems(m, request.user, serializer.data['uuid'])
            return Response({'result':a})
        elif requirements == 'total price':
            if store.PrintTagItems.price > serializer.data['total']:
                collectItems(serializer.data['items'])
        elif requirements == 'category':
            m = []
            for i in serializer.data['items']:
                if i.category in store.PrintTagItems.category:
                    m.append(i)
            collectItems(m)
        elif requirements == 'select':
            m = []
            for i in serializer.data['items']:
                if i in PrintTagItems.items:
                    m.append(i)
            collectItems(m)

def ValidateReturnResultTag(request):
    try:
        tag = ResultTag.objects.get(lookup_code=lookup)
        items = request.data['items']

    except ResultTag.DoesNotExist:
        raise Response({'outcome':'result tag invalid or does not exist'})







"""
action tasks
"""


"""
simple tasks
"""
#PrintTagItems crud
class createPrintTagItems(CreateView):
    model = PrintTagItems
    fields = ['requirements', 'items', 'price', 'categories']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.store = self.request.user.store
        return super(videoCreate, self).form_valid(form)

def editPrintTagItems(request, uuid):
    if request.method == 'POST':
        item = PrintTagItems.objects.get(uuid=uuid)
        form = PrintTagItemsForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('product:home'))

        else:
            #messages.error(request, "Error")
            return render(request, 'product/create.html', {'form':form})

    else:
        form = RegistrationForm(instance=item)
        return render(request, 'product/create.html', {'form':form})

def deletePrintTagItems(request, uuid):
    try:
        Item = PrintTagItems.objects.get(uuid=uuid)
        if item in request.user.store.item_set.all():
            item.delete()
    except Item.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('product:home'))

def retrievePrintTagItems(request, uuid):
    try:
        query = PrintTagItems.objects.get(uuid=uuid)
    except Item.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'product/view.html', {'query':query})


#store crud
class editStore(UpdateView):
    model = Store
    fields = ['name', 'state', 'street', 'street2', 'phone_number', 'zip_code']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(videoCreate, self).form_valid(form)

#item crud
class createItem(CreateView):
    model = Item
    fields = ['name', 'price', 'category', 'on_sale', 'weight']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.store = self.request.user.store
        return super(videoCreate, self).form_valid(form)

def editItem(request, uuid):
    if request.method == 'POST':
        item = Item.objects.get(uuid=uuid)
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('product:home'))

        else:
            #messages.error(request, "Error")
            return render(request, 'product/create.html', {'form':form})

    else:
        form = RegistrationForm(instance=item)
        return render(request, 'product/create.html', {'form':form})

def deleteItem(request, uuid):
    try:
        Item = Item.objects.get(uuid=uuid)
        if item in request.user.store.item_set.all():
            item.delete()
    except Item.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('product:home'))

def retrieveItem(request, uuid):
    try:
        query = Item.objects.get(uuid=uuid)
    except Item.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'product/view.html', {'query':query})

def listItem(request):
    qs = Item.objects.filter(store=request.user.store)
    return render(request, 'product/view.html', {'qs':qs})


#category crud
class createCategory(CreateView):
    model = Category
    fields = ['name', 'return_policy']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.store = self.request.user.store
        return super(createCategory, self).form_valid(form)

def editCategory(request, uuid):
    if request.method == 'POST':
        item = Category.objects.get(uuid=uuid)
        form = CategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('product:home'))

        else:
            #messages.error(request, "Error")
            return render(request, 'product/create.html', {'form':form})

    else:
        form = CategoryForm(instance=item)
        return render(request, 'product/create.html', {'form':form})

def deleteCategory(request, uuid):
    try:
        Item = Category.objects.get(uuid=uuid)
        if item in request.user.store.item_set.all():
            item.delete()
    except Item.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('product:home'))

def retrieveCategory(request, uuid):
    try:
        query = Category.objects.get(uuid=uuid)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    return render(request, 'product/detail.html', {'query':query})

def listCategory(request):
    qs = Category.objects.filter(store=request.user.store)
    return render(request, 'product/view.html', {'qs':qs})


#return policy crud
class createReturnPolicy(CreateView):
    model = ReturnPolicy
    fields = ['elapse_days', 'holiday_elapse_days', 'apply_to_sales']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.store = self.request.user.store
        return super(createReturnPolicy, self).form_valid(form)

def editReturnPolicy(request, uuid):
    if request.method == 'POST':
        item = ReturnPolicy.objects.get(uuid=uuid)
        form = ReturnPolicyForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('product:home'))

        else:
            #messages.error(request, "Error")
            return render(request, 'product/create.html', {'form':form})

    else:
        form = RegistrationForm(instance=item)
        return render(request, 'product/create.html', {'form':form})

def deleteReturnPolicy(request, uuid):
    try:
        Item = ReturnPolicy.objects.get(uuid=uuid)
        if item in request.user.store.item_set.all():
            item.delete()
    except ReturnPolicy.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('product:home'))

def retrieveReturnPolicy(request, uuid):
    try:
        query = ReturnPolicy.objects.get(uuid=uuid)
    except ReturnPolicy.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'product/view.html', {'query':query})


"""
def updateParentStore(request):
    if request.method  == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        form1 = updateParentStoreForm(request.POST, request.FILES, instance=request.user.parentStore)
        if form.is_valid() and form1.is_valid():
            #profile = form.save(commit=False)
            #profile.first_name = form.cleaned_data['first_name']
            #profile.last_name = form.cleaned_data['last_name']
            #profile.email = form.cleaned_data['email']
            form.save()
            form1.save()
            return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
        else:
            #messages.error(request, "Error")
            return render(request, 'pages/2/signup.html', {'form':form})

    else:
        form = EditProfileForm(instance=request.user)
        form1 = UpdateUserForm(instance=request.user.profile)
        return render(request, 'pages/5/editprofile.html', {'form':form, 'form1':form1})



#employee crud
class createEmployee(CreateView):
    model = ParentStore
    fields = ['employee_identifier', 'employee_name']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.store = self.request.user.store
        return super(videoCreate, self).form_valid(form)




#on sale crd
class createOn_Sale(CreateView):
    model = On_Sale
    fields = ['first_active_date', 'last_active_date']
    template_name = 'product/create.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.store = self.request.user.store
        return super(createOn_Sale, self).form_valid(form)
"""
