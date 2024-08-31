import django_filters
from base.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    short_description = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    store = django_filters.CharFilter(field_name='id')
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='id'
    )

    class Meta:
        model = Product
        fields = ['name', 'short_description',
                  'description', 'price', 'store', 'categories']
