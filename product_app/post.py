from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, ProductCategory, Variations, VariationOption, ProductItem, Stock, ProductImage
from .serializers import ProductSerializer, ProductCategorySerializer, VariationsSerializer, VariationOptionSerializer, ProductItemSerializer, StockSerializer, ProductImageSerializer


@api_view(['GET'])
def get_product_by_id(request, pk=None):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except product.DoesNotExist:
       return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_categories_by_product(request, pk=None):
    product = Product.objects.get(id = pk)
    try:
        categories = product.categories.all()
        serializer = ProductCategorySerializer(data=categories)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except product.DoesNotExist:
       return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_variations_by_category(request, pk=None):
    category = ProductCategory.objects.get(id=pk)
    try:
        variations = Variations.objects.filter(category_id = category.id)
        serializer = VariationsSerializer(data=variations)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except category.DoesNotExist:
       return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'PUT', 'POST'])
def post_product(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Retrieve the existing product
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Link the existing categories
        
        category_data = request.data.get('category')
        if category_data:
            for category in category_data:
                try:
                    category_instance = ProductCategory.objects.get(
                        id=category['id'])
                    
                    product.categories.add(category_instance)
                except ProductCategory.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

        # Link the existing variations and their options
        variation_option = []
        variation_data = request.data.get('variation')
        if variation_data:
            for variation in variation_data:
                try:
                    variation_instance = Variations.objects.get(
                        id=variation['id'])
                    for option in variation.get('options', []):
                        try:
                            option_instance = VariationOption.objects.get(
                                id=option['id'])
                            variation_instance.options.add(option_instance)
                            variation_option.append(option_instance.id)
                        except VariationOption.DoesNotExist:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                except Variations.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

        # create Product Items
        product_item = ProductItem.objects.create(
            product=product)
        

        # Add stock based on the linked variations
        stock_data = request.data.get('stock')
        if stock_data:
            for item in stock_data:
                try:
                    product_item = ProductItem.objects.get(
                        id=item['product_item_variation'])
                except ProductItem.DoesNotExist:
                    item_data = {**item, 'product': product.id}
                    item_serializer = ProductItemSerializer(data=item_data)
                    if item_serializer.is_valid():
                        product_item = item_serializer.save()
                    else:
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                stock_data = {
                    **item, 'product_item_variation': product_item.id}
                stock_serializer = StockSerializer(data=stock_data)
                if stock_serializer.is_valid():
                    stock_serializer.save()
                else:
                    return Response(stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create new ProductImage instances and link them to the product
        image_data = request.data.get('productImage')
        if image_data:
            for image in image_data:
                image_data = {**image, 'product': product.id}
                image_serializer = ProductImageSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product_data = request.data.get('product')
        product_serializer = ProductSerializer(
            product, data=product_data, partial=True)
        if product_serializer.is_valid():
            product = product_serializer.save()
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Link the existing categories
        category_data = request.data.get('category')
        if category_data:
            for category in category_data:
                try:
                    category_instance = ProductCategory.objects.get(
                        id=category['id'])
                    product.categories.add(category_instance)
                except ProductCategory.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

        # Link the existing variations and their options
        variation_data = request.data.get('variation')
        if variation_data:
            for variation in variation_data:
                try:
                    variation_instance = Variations.objects.get(
                        id=variation['id'])
                    for option in variation.get('options', []):
                        try:
                            option_instance = VariationOption.objects.get(
                                id=option['id'])
                            variation_instance.options.add(option_instance)
                        except VariationOption.DoesNotExist:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                except Variations.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

        # Add stock based on the linked variations
        stock_data = request.data.get('stock')
        if stock_data:
            for item in stock_data:
                try:
                    product_item = ProductItem.objects.get(
                        id=item['product_item_variation'])
                except ProductItem.DoesNotExist:
                    item_data = {**item, 'product': product.id}
                    item_serializer = ProductItemSerializer(data=item_data)
                    if item_serializer.is_valid():
                        product_item = item_serializer.save()
                    else:
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                stock_data = {
                    **item, 'product_item_variation': product_item.id}
                stock_serializer = StockSerializer(data=stock_data)
                if stock_serializer.is_valid():
                    stock_serializer.save()
                else:
                    return Response(stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create new ProductImage instances and link them to the product
        image_data = request.data.get('productImage')
        if image_data:
            for image in image_data:
                image_data = {**image, 'product': product.id}
                image_serializer = ProductImageSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(product_serializer.data)
