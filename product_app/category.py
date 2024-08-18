
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from base.models import *
from .serializers import *

User = get_user_model()

@api_view(['GET', 'POST', 'DELETE'])
def category_management(request, pk=None):
    try:
        store = Store.objects.get(id=pk)
    except Store.DoesNotExist:
        return Response({'detail': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        categories = Category.objects.all()
        if categories:
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No categories found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        category_data = request.data
        category_data['store'] = store.id  # Include store data
        serializer = CategorySerializer(data=category_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            category = Category.objects.get(id=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_one_category_and_create_detail_variations(request, pk=None):
    if request.method == 'GET':
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Unexpected error: {e}')
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            category = Category.objects.get(pk=pk)
            data = request.data
            attribute_type = data.get('attribute_type')
            options = data.get('options', [])

            if not attribute_type or not isinstance(options, list) or not options:
                return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

            # Create or get the variation instance and associate it with the category
            variation, created = Variations.objects.get_or_create(
                attribute_type=attribute_type,
                category=category
            )

            # Create the variation options
            for option in options:
                value = option.get('value')
                if value:
                    VariationOption.objects.create(
                        variation=variation,
                        value=value
                    )

            return Response({'detail': 'Variation options created successfully'}, status=status.HTTP_201_CREATED)

        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Unexpected error: {e}')
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_variations_use_category(request, pk=None):
    try:
        category = Category.objects.get(id=pk)
        variations = Variations.objects.filter(category=category)

        # Create a list to hold the serialized variations with nested options
        serialized_variations = []

        for variation in variations:
            options = VariationOption.objects.filter(variation=variation)
            variation_data = {
                "id": variation.id,
                "attribute_type": variation.attribute_type,
                "variation_option": VariationOptionSerializer(options, many=True).data
            }
            serialized_variations.append(variation_data)

        return Response(serialized_variations, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
