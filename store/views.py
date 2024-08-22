from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from base.models import Store, Publish, Product, Draft, CustomerList
from .serializers import *
from base.models import *
User = get_user_model()


@api_view(['GET', 'POST', 'PUT'])
def store_view(request, pk=None):
    if request.method == 'GET':
        try:
            store = Store.objects.get(seller=pk)
            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            user = User.objects.get(id=pk)
            request.data['seller'] = pk
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not pk:
            return Response({'error': 'Store ID is required for update'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('seller')
        if not user_id:
            return Response({'error': 'Seller ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            request.data['seller'] = user.id
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_publish_by_store(request, pk=None):
    store = Store.objects.get(id=pk)
    try:
        publish = Publish.objects.filter(store=store)
        products = []
        for pub in publish:
            product = Product.objects.get(id=pub.product.id)
            products.append(product)
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_draft_by_store(request, pk=None):
    store = Store.objects.get(id=pk)
    try:
        publish = Draft.objects.filter(store=store)
        products = []
        for pub in publish:
            product = Product.objects.get(id=pub.product.id)
            products.append(product)
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_cutomers_by_store(request, pk=None):
    store = Store.objects.get(id=pk)
    try:
        customers = CustomerList.objects.filter(store=store)
        serializers = CustomerListSerializer(customers, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_product_detail(request, pk=None):
    try:
        # Get the product
        product = Product.objects.get(id=pk)

        # Serialize the product itself
        product_data = ProductSerializer(product).data

        # Get and serialize product categories
        categories = product.categories.all()
        categories_data = CategorySerializer(categories, many=True).data

        # variation data

        variations = Variations.objects.filter(category=categories[0].id)
        # variation option with quantity from stock
        variation_data_list = []
        # Get and serialize stock data
        for variation in variations:
            options = VariationOption.objects.filter(variation=variation)
            option_list = []
            for option in options:
                try:
                    stock = Stock.objects.filter(
                        product=product, variation_option_id=option.id).first()
                    stock_data = StockSerializer(stock).data
                    print(stock)
                    option_list.append({
                        'option': option.value,
                        'stock': stock_data
                    })
                except Stock.DoesNotExist:
                    option_list.append({
                        'option': option.value,
                        'stock': None
                    })
            variation_data_list.append({
                'attribute_type': variation.attribute_type,
                'options': option_list
            })

        # Get and serialize product images
        images = ProductImage.objects.filter(product=product)
        images_data = ProductImageSerializer(images, many=True).data

        # Combine all the data into one dictionary
        response_data = {
            "product": product_data,
            "categories": categories_data,
            "variations": variation_data_list,
            "images": images_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_categories(request):
    query = request.GET.get('q', '')
    if query:
        categories = Category.objects.filter(
            Q(category_name__icontains=query) |
            Q(image__icontains=query)
        )
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    return Response({"message": "No query provided."})


@api_view(['GET', 'POST'])
def save_store_category(request, pk):
    try:
        store = Store.objects.get(id=pk)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        store_categories = StoreCategory.objects.filter(store=store.id)
        categories = []
        for store_cat in store_categories:
            category = Category.objects.get(id=store_cat.categories.id)
            categories.append(category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        category_id = request.query_params.get('category')
        if not category_id:
            return Response({"error": "Category ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ins_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        store_category = StoreCategory.objects.update_or_create(
            categories=ins_category,
            store=store
        )
        return Response({"message": "Category added to store"}, status=status.HTTP_201_CREATED)
