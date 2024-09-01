from rest_framework import generics
from .filters import ProductFilter
from .serializers import ProductSerializer
from base.models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q


from base.models import ProductImage
from product_app.serializers import ProductImageSerializer
from .services.image_processing import extract_image_features, compare_images


class UploadAndMatchImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if not request.FILES.get('image'):
            return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_image = request.FILES['image']

        # Step 1: Extract features from the uploaded image
        uploaded_features = extract_image_features(
            uploaded_image.temporary_file_path())

        # Step 2: Compare with all stored product images
        product_images = ProductImage.objects.exclude(features=None)
        best_match = None
        highest_similarity = 0

        for product_image in product_images:
            similarity = compare_images(
                uploaded_features, product_image.features)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = product_image

        if best_match:
            serializer = ProductImageSerializer(best_match)
            return Response({
                'product': serializer.data['product'],
                'image_url': serializer.data['image'],
                'similarity_score': highest_similarity
            })
        else:
            return Response({'error': 'No matching product found'}, status=status.HTTP_404_NOT_FOUND)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', None)
    products_starting_with_name = Product.objects.none()
    products_containing_query = Product.objects.none()

    if query:
        # Step 1: Products where name starts with the query
        products_starting_with_name = Product.objects.filter(
            name__istartswith=query)

        # Step 2: Products where name, short_description, or description contains the query
        products_containing_query = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        ).exclude(id__in=products_starting_with_name.values('id'))

    # Combine both querysets
    products = products_starting_with_name | products_containing_query

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def product_relate(request, pk):
    cat = Product.objects.filter(                 )

