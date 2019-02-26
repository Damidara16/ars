from rest_framework import serializers

class Answers(serializer.Serializers):
    q1 = serializers.BooleanField(default=False, required=True)
    q2 = serializers.BooleanField(default=False, required=True)
    onSale = serializers.BooleanField(default=False, required=True)
    tagId = serializers.CharField(max_length=255, required=True)
    #weight = serializers.CharField(max_length=255, required=True)
    category = serializers.CharField(max_length=255, required=True)
    itemName = serializers.CharField(max_length=255, required=True)
    reason = serializers.CharField(max_length=255, required=True)
    price = serializers.CharField(max_length=255, required=True)
    method = serializers.CharField(max_length=255, required=True)
    last4 = serializers.CharField(max_length=255)
    storeId = serializers.CharField(max_length=255, required=True)
    timeBought = serializers.CharField(max_length=255, required=True)
