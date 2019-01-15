from django.shortcuts import render
from product.models import *
from rest_framework.response import Response

# Create your views here.
def verify(request):
    lc = request.POST.get('q')
    lc2 = request.POST.get('e')
    try:
        a = ReturnTag.objects.get(lookup_code=lc)
        b = PurchaseTag.objects.get(lookup_code=lc2)
        if a.exists() and a.purchase_tag == b:
            return render(request, 'quiz/verified.html')
        else:
            return render(request, 'quiz/unverified.html')
    except ReturnTag.DoesNotExist or PurchaseTag.DoesNotExist:
            return render(request, 'quiz/unverified.html')

def preverify(request):
    return render(request, 'quiz/verify.html')
