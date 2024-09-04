from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, UserReview, User
from .serializers import UserReviewSerializer


@api_view(['POST'])
def create_comment(request):
    try:
        user_id = request.query_params.get('user')
        product_id = request.query_params.get('product')
        # Assuming comment is passed in the body of the request
        comment_text = request.data.get('comment')

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        # Get or create the UserReview
        review, created = UserReview.objects.get_or_create(
            user=user,
            product=product,
            defaults={'comment': comment_text}
        )

        if not created:
            # If the review already exists, you might want to update the comment
            review.comment = comment_text
            review.save()

        return Response({
            'message': 'Comment created' if created else 'Comment updated',
            'review': {
                'user': review.user.id,
                'product': review.product.id,
                'comment': review.comment,
            }
        }, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_comments(request):
    product_id = request.query_params.get('product')

    try:
        product = Product.objects.get(id=product_id)
        comments = UserReview.objects.filter(product=product)
        
        serializer = UserReviewSerializer(comments, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

