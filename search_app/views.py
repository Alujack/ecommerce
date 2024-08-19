from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

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
