from django.contrib.auth.models import User, update_last_login
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework.response import Response


from base.products import products
from base.models import Product,Order, OrderItem,ShippingAddress
from base.serializer import ProductSerializer,OrderSerializer
# Create your views here.

from django.contrib.auth.hashers import make_password
from rest_framework import status

from base import serializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):

    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) ==0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        #create order
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        #create shipping address
        shipping = ShippingAddress.objects.create(
            order= order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country']

        )
        #create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])


            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url
            )

            #4 update stock
            product.countInStock = int(product.countInStock)- int(item.qty)
            product.save()


        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getOrderById(request, pk):
    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
           serializer = OrderSerializer(order, many=False)
           return Response(serializer.data)
        else:
           return Response({'detail':'Not authorized to view this order'},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail':'Order does not exist'},status=status.HTTP_400_BAD_REQUEST)



