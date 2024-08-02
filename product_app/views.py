from rest_framework import generics
from .serializers import ProductSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from base.models import ProductCategory, Store, Stock, Product, VariationOption,Variations
from .serializers import ProductSerializer, ProductCategorySerializer,VariationOptionSerializer
User = get_user_model()


@api_view(['GET', 'POST', 'DELETE'])
def category_management(request, pk=None):
    if request.method == 'GET':
        categories = ProductCategory.objects.all()
        if categories:
            serializer = ProductCategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No categories found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        category = request.data
        serializer = ProductCategorySerializer(data=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            category = ProductCategory.objects.get(id=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_one_category_and_create_detail_variations(request, pk=None):
    if request.method == 'GET':
        try:
            category = ProductCategory.objects.get(pk=pk)
            serializer = ProductCategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Unexpected error: {e}')
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            category = ProductCategory.objects.get(pk=pk)
            data = request.data
            attribute_type = data.get('attribute_type')
            options = data.get('options', [])

            if not attribute_type or not isinstance(options, list) or not options:
                return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

            # Create or get the variation instance
            variation, created = Variations.objects.get_or_create(
                attribute_type=attribute_type
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

        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Unexpected error: {e}')
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
