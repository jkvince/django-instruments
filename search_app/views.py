from shop.models import Product
from django.views.generic import ListView
from django.db.models import Q

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:  # Ensure query is not None or empty
            return Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView,self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context