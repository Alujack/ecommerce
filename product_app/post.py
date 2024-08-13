
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, ProductCategory, Variations, VariationOption, ProductItem, Stock, ProductImage, Publish, Draft
from .serializers import ProductSerializer, ProductCategorySerializer, VariationsSerializer, VariationOptionSerializer, ProductItemSerializer, StockSerializer, ProductImageSerializer
from django.shortcuts import get_object_or_404
import json


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


@api_view(['POST'])
def post_product(request, pk=None):
    try:
        # print(request.store)
        data = request.data
        # # Retrieve the product by its ID
        product = get_object_or_404(Product, id=pk)

        # # Handle product items
        product_items_data = data.get('product_items', [])

        for item_data in product_items_data:
            variation_option_id = item_data['variation_option']
            if not variation_option_id:
                return Response({"error": "Missing variation option ID."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the VariationOption instance
            variation_option = get_object_or_404(
                VariationOption, id=variation_option_id)

        #     # Create or retrieve the ProductItem
            product_item, created = ProductItem.objects.get_or_create(
                product=product,
                variation_option=variation_option
            )

            if created:
                print(f"ProductItem created: {product_item}")
            else:
                print(f"ProductItem already exists: {product_item}")

        # # Handle product images
        # Extract and parse the JSON data from the request
        product_image_data = data.get('product_images')
        if product_image_data:
            product_image_data = json.loads(product_image_data)

        # Handle the files
        product_images_data = []
        for key in request.data:
            if key.startswith('product_images'):
                index = key.split('[')[1].split(']')[0]
                field = key.split('][')[1][:-1]
                if len(product_images_data) <= int(index):
                    product_images_data.append({})
                product_images_data[int(index)][field] = request.data[key]

        # Handle the files
        for image_data in product_images_data:
            if image_data.get('url'):
                product_image_data = {
                    'product': '9fec4cd5a5e643abb2483dde9fa1fbee',
                    'image': image_data['url'],
                    'angle': image_data.get('angle', ''),
                }
                serializer = ProductImageSerializer(data=product_image_data)
                if serializer.is_valid():
                    serializer.save()
                    print(f"ProductImage created: {serializer.data}")
                else:
                    print(f"ProductImage creation failed: {serializer.errors}")
            else:
                print("No valid image file found in image_data")

        #  Handle stocks for each product item
        stocks_data = data.get('stocks', [])

        for stock_data in stocks_data:
            product_item_variation = stock_data['product_item_variation']

            if not product_item_variation:
                return Response({"error": "Missing product item variation data."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the correct ProductItem
            product_item = ProductItem.objects.get(
                product=product_item_variation['product'],
                variation_option=product_item_variation['variation_option']
            )

            # Create Stock
            stock = Stock.objects.create(
                quantity=stock_data['quantity'],
                product_item_variation=product_item,
                store=product.store
            )
        publish = Publish.objects.update_or_create(
            product=product,
            store=product.store)

        try:
            draft_delete = Draft.objects.get(product=product)
            if draft_delete:
                draft_delete.delete()
        except:
            pass
        return Response({"success": "Product items, stocks, and images created successfully."}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
