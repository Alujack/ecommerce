from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from base.models import ShopOrder, OrderLine, Address, PaymentMethod, PaymentType, CreditCard, BankInformation, ShippingMethod, Coupon, User
from .serializers import ShopOrderSerializer, OrderLineSerializer
from django.core.exceptions import ValidationError
from decimal import Decimal


def apply_coupon(coupon_code, order_total):
    """
    Apply the coupon and return the discount amount.
    """
    try:
        coupon = Coupon.objects.get(code=coupon_code, active=True)
        discount_amount = order_total * \
            Decimal(coupon.discount_percentage) / 100
        return discount_amount
    except Coupon.DoesNotExist:
        return Decimal(0)


def calculate_order_total(products, coupon_code, shipping_method):
    """
    Calculate the total cost of the order.
    """
    order_total = Decimal(0)

    for product in products:
        order_total += Decimal(product['price']) * product['quantity']

    if shipping_method:
        order_total += Decimal(shipping_method.price)

    discount_amount = Decimal(0)
    if coupon_code:
        discount_amount = apply_coupon(coupon_code, order_total)
        order_total -= discount_amount

    return order_total, discount_amount


def process_payment(order):
    """
    Process the payment for the given order.
    """
    # Placeholder for payment processing
    payment_successful = True
    if not payment_successful:
        raise ValidationError("Payment failed. Please try again.")
    order.status = 'processing'
    order.save()


@api_view(['POST'])
def create_order(request):
    data = request.data

    try:
        # Extract customer, products, and shipping details
        customer = data.get('customer')
        products = data.get('order_lines')
        shipping_address_data = data.get('shipping_address')
        shipping_method_id = data.get('shipping_method')
        coupon_code = data.get('coupon_code')
        payment_type = data.get('payment_type')
        customer = User.objects.get(id=customer)

        # Handle Shipping Address Creation
        shipping_address, created = Address.objects.update_or_create(
            house_number=shipping_address_data.get('house_number'),
            street_number=shipping_address_data.get('street_number'),
            village=shipping_address_data.get('village'),
            commune=shipping_address_data.get('commune'),
            district=shipping_address_data.get('district'),
            city=shipping_address_data['city'],
            postal_code=shipping_address_data['postal_code'],
            country=shipping_address_data['country'],
            phone_number=shipping_address_data['phone_number'],
        )

        # Handle Payment Method Creation

        payment_types = PaymentType.objects.get(id=payment_type)
        card_details = data.get('credit_card')
        bank_details = data.get('bank')
        if card_details:
            cart_provider, _ = CreditCard.objects.update_or_create(
                payment_type_id=payment_types.id,
                card_holder_name=card_details['card_holder_name'],
                card_number=card_details['card_number'],
                expired_date=card_details['expired_date'],
                cvv=card_details['cvv']
            )
        if bank_details:
            bank_provider, _ = BankInformation.objects.update_or_create(
                payment_type_id=payment_types.id,
                acc_holder_name=bank_details['acc_holder_name'],
                acc_number=bank_details['acc_number'],
                bank_name=bank_details['bank_name'],
                routing_number=bank_details['routing_number'],
                iban=bank_details['iban']
            )

        if payment_types.type_value == 'cart':
            payment_method, create = PaymentMethod.objects.update_or_create(
                customer_id=customer.id,
                provider_card=cart_provider
            )
        elif payment_types.type_value == 'bank':
            payment_method, create = PaymentMethod.objects.update_or_create(
                customer_id=customer,
                provider_bank=bank_provider
            )

        # Fetch ShippingMethod instance
        shipping_method = ShippingMethod.objects.get(id=shipping_method_id)

       # Calculate the order total and discount amount
        order_total, discount_amount = calculate_order_total(
            products, coupon_code, shipping_method)

        # Retrieve the payment method instance
        payment_method_ins = PaymentMethod.objects.get(id=payment_method.id)

        # Create the ShopOrder
        order, _ = ShopOrder.objects.update_or_create(
            customer=customer,
            payment_method=payment_method_ins,
            shipping_address=shipping_address,
            shipping_method=shipping_method,
            order_total=order_total,
            discount_amount=discount_amount
        )
        for product in products:
            OrderLine.objects.create(
                product_id=product['product'],
                order=order,
                quantity=product['quantity'],
                price=product['price']
            )

        # Process payment
        process_payment(order)

        # Serialize the response
        serializer = ShopOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
