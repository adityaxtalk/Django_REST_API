from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view

from product.models import Product
from product.serializers import ProductSerializer

@api_view(['GET','POST','DELETE'])
def product_list(request):
    if request.method=='GET':
        products=Product.objects.all()
        title=request.query_params.get('title',None)
        if title is not None:
            products=products.filter(title__icontains=title)
        
        product_serializer=ProductSerializer(products,many=True)
        return JsonResponse(product_serializer.data,safe=False)
    
    elif request.method=='POST':
        product_data=JSONParser().parse(request)
        product_serializer=ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        count=Product.objects.all().delete()
        return JsonResponse({'message':f'{count[0]} Products are deleted successfully!'})



@api_view(['GET','PUT','DELETE'])
def product_detail(request,pk):
    try:
        product=Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'message':'The product does not exist',status:status.HTTP_404_NOT_FOUND})
    
    if request.method=='GET':
        product_serializer=ProductSerializer(product)
        return JsonResponse(product_serializer.data)
    
    elif request.method=='PUT':
        product_data=JSONParser().parse(request)
        product_serializer=ProductSerializer(product,data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data)
        return JsonResponse(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
         product.delete()
         return JsonResponse({'message': 'Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)      