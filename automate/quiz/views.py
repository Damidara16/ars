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


@api_view(['POST'])
def createReturnTag(request, aws=[]):
    serializer = Answers(request.data)
    if serializer.is_valid():
        rates = []
        if serializer.data['q1'] or serializer.data['q2'] == False:
            return Response({'outcome':'return not up to standards of our return policy'})
        id = serializer.data['tagId']
        a = PurchaseTag.objects.get(lookup_code=id)
        if a.exists():
            rates.append(10)



        result = sum(rates)/len(rates)

        if result > request.user.PrintTagItems.limit:
            b = ReturnTag.objects.create()
            return Response({'outcome':b.lookup_code})
{
q1:,
q2:,
onSale:,
tagId:,
wieght:,
category:,
itemName:,
reason:,
price:,
method:,
last4:,
storeId:,
timeBought:
}
