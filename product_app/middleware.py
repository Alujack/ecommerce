from django.utils.deprecation import MiddlewareMixin
from base.models import Store


class StoreMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.store = Store.objects.filter(seller=request.user).first()
        else:
            request.store = None
