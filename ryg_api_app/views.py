from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, UserPermission
from .serializers import ProductSerializer
def test_json_view(request):
    data = {
        'name': 'John Doe',
        'age': 30,
        'location': 'New York',
        'is_active': True,
    }
    return JsonResponse(data)

@csrf_exempt
def post_json_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_name = body.get('user', 'Unknown')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        data = {
            'name': user_name,
            'age': 30,
            'location': 'New York',
            'is_active': True,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    # Vérifier que l'utilisateur connecté a des permissions
    if not hasattr(request.user, 'userpermission') or not request.user.userpermission.can_view_products:
        return Response({'error': 'Permission denied'}, status=403)
    products = Product.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 3
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_most_expensive_product(request):
    # Vérifier que l'utilisateur connecté a des permissions
    if not hasattr(request.user, 'userpermission') or not request.user.userpermission.can_view_products:
        return Response({'error': 'Permission denied'}, status=403)
    product = Product.objects.order_by('-price')[:10]
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    print(f"Utilisateur connecté : {request.user}")

    try:
        permission = UserPermission.objects.get(user=request.user)
        print(f"can_add_products = {permission.can_add_products}")
        print(f"Permissions : {permission}")
    except UserPermission.DoesNotExist:
        print("Pas de permission associée")
        return Response({'error': 'Permission denied'}, status=403)

    if not permission.can_add_products:
        print("Permission d’ajout refusée")
        return Response({'error': 'Permission denied'}, status=403)

    print(f"Utilisateur connecté : {request.user} ({type(request.user)})")
    print(UserPermission.objects.filter(user=request.user).exists())

    # Vérifier que l'utilisateur connecté a des permissions
    if not hasattr(request.user, 'userpermission') or not request.user.userpermission.can_view_products:
        return Response({'error': 'Permission denied'}, status=403)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    # Vérifier que l'utilisateur connecté a des permissions
    if not hasattr(request.user, 'userpermission') or not request.user.userpermission.can_view_products:
        return Response({'error': 'Permission denied'}, status=403)
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product does not exist'}, status=404)
    serializer = ProductSerializer(product,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
