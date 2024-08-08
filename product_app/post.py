
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, ProductCategory, Variations, VariationOption, ProductItem, Stock, ProductImage, Publish, Draft
from .serializers import ProductSerializer, ProductCategorySerializer, VariationsSerializer, VariationOptionSerializer, ProductItemSerializer, StockSerializer, ProductImageSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_product_by_id(request, pk=None):

    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product)
    if serializer:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_categories_by_product(request, pk=None):
    product = Product.objects.get(id=pk)
    try:
        categories = product.categories.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except product.DoesNotExist:
        return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_variations_by_category(request, pk=None):
    category = ProductCategory.objects.get(id=pk)
    try:
        variations = Variations.objects.filter(category_id=category.id)
        serializer = VariationsSerializer(variations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except category.DoesNotExist:
        return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_options_by_variation(request, pk=None):
    variation = Variations.objects.get(id=pk)
    try:
        options = VariationOption.objects.filter(variation_id=variation.id)
        serializers = VariationOptionSerializer(options, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except variation.DoesNotExist:
        return Response(serializers.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_variations_and_Options_id(request, pk=None):
    try:
        variation = Variations.objects.get(id=pk)
        # Create a list to hold the serialized variations with nested options
        serialized_variations = []
        options = VariationOption.objects.filter(variation=variation)
        variation_data = {
            "id": variation.id,
            "attribute_type": variation.attribute_type,
            "variation_option": VariationOptionSerializer(options, many=True).data
        }
        serialized_variations.append(variation_data)

        return Response(serialized_variations, status=status.HTTP_200_OK)
    except ProductCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'POST'])
def post_product(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            data = request.data

            print("Converted request data:", data)

            # Retrieve the product by its ID
            product = get_object_or_404(Product, id=pk)
            print(f"Product retrieved: {product}")

            # Handle product items
            product_items_data = data.get('product_items', [])
            print(f"Product items data: {product_items_data}")

            for item_data in product_items_data:
                variation_option_id = item_data.get('variation_option')
                if not variation_option_id:
                    return Response({"error": "Missing variation option ID."}, status=status.HTTP_400_BAD_REQUEST)

                variation_option = get_object_or_404(
                    VariationOption, id=variation_option_id)
                print(f"VariationOption retrieved: {variation_option}")

                # Create the ProductItem and link it to the VariationOption
                product_item, created = ProductItem.objects.get_or_create(
                    product=product,
                    variation_option=variation_option
                )
                if created:
                    print(f"ProductItem created: {product_item}")
                else:
                    print(f"ProductItem already exists: {product_item}")

            # Handle stocks for each product item
            stocks_data = data.get('stocks', [])
            print(f"Stocks data: {stocks_data}")

            for stock_data in stocks_data:
                product_item_variation = stock_data.get(
                    'product_item_variation')
                if not product_item_variation:
                    return Response({"error": "Missing product item variation data."}, status=status.HTTP_400_BAD_REQUEST)

                product_item = get_object_or_404(ProductItem,
                                                 product=product_item_variation['product'],
                                                 variation_option=product_item_variation['variation_option']
                                                 )
                print(f"ProductItem retrieved for stock: {product_item}")

                stock = Stock.objects.create(
                    quantity=stock_data['quantity'],
                    product_item_variation=product_item,
                    store=product.store
                )
                print(f"Stock created: {stock}")

            # Handle product images
            product_images_data = data.get('product_images', [])
            print(f"Product images data: {product_images_data}")

            for image_data in product_images_data:
                if image_data.get('url'):
                    product_image = ProductImage.objects.create(
                        product=product,
                        image=image_data['url'],
                        angle=image_data.get('angle', '')
                    )
                    print(f"ProductImage created: {product_image}")

            return Response({"success": "Product items, stocks, and images created successfully."}, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except VariationOption.DoesNotExist:
            return Response({"error": "Variation option not found."}, status=status.HTTP_404_NOT_FOUND)
        except ProductItem.DoesNotExist:
            return Response({"error": "Product item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        # Link the existing category
        category_id = request.data.get('categoryId')
        if category_id:
            try:
                category_instance = ProductCategory.objects.get(id=category_id)
                product.categories.add(category_instance)
            except ProductCategory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        # Link the existing variations and their options
        variation_data = request.data.get('variations')
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
        stock_data = request.data.get('stocks')
        if stock_data:
            for item in stock_data:
                try:
                    product_item = ProductItem.objects.get(
                        id=item['product_item_variation']['id'])
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
        image_data = request.data.get('productImages')
        if image_data:
            for image in image_data:
                if image['url']:
                    image_data = {**image, 'product': product.id}
                    image_serializer = ProductImageSerializer(data=image_data)
                    if image_serializer.is_valid():
                        image_serializer.save()
                    else:
                        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(product_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def publish_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    print(request.store)  # Print the request data for debugging

    # Create a new Publish instance
    publish = Publish.objects.update_or_create(
        product=product,
        store=product.store
    )

    # Return a Response object
    return Response({"success": "Product published successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def draft_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    print(request.store)  # Print the request data for debugging

    # Create a new Publish instance
    draft = Draft.objects.update_or_create(
        product=product,
        store=product.store
    )

    # Return a Response object
    return Response({"success": "Product published successfully."}, status=status.HTTP_201_CREATED)