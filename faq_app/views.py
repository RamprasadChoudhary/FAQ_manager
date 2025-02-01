import logging
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer

logger = logging.getLogger(__name__)

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        logger.info("Executing FAQ list view")
        response = super().list(request, *args, **kwargs)
        cache_key = request.path
        logger.info(f"Cache key: {cache_key}")
        cache_value = cache.get(cache_key)
        logger.info(f"Cache hit: {cache_value is not None}")
        return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context