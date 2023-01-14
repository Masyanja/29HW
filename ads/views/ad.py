from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, filters, status, viewsets, request

from ads.models import Ad, Category
from avito import settings
from ads.serializers import (
    AdSerializer,
    AdCreateSerializer,
    AdUpdateSerializer,
    AdDeleteSerializer,
    CategorySerializer,
)


def root(request):
    return JsonResponse({
        "status": "ok"
    })


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    class AdView(ListView):
        model = Ad
        queryset = Ad.objects.all()

        def get(self, request, *args, **kwargs):
            super().get(request, *args, **kwargs)

            categories = request.GET.getlist('cat', None)
            if categories:
                self.object_list = self.object_list.filter(category_id__in=categories)

            text = request.GET.get('text', None)
            if text:
                self.object_list = self.object_list.filter(name__icontains=text)

            location = request.GET.get("location", None)
            if location:
                self.object_list = self.object_list.filter(author__location__name__icontains=location)

            price_from = request.GET.get('price_from', None)
            if price_from:
                self.object_list = self.object_list.filter(price__gte=price_from)

            price_to = request.GET.get('price_to', None)
            if price_to:
                self.object_list = self.object_list.filter(price__lte=price_to)

            self.object_list = self.object_list.select_related('author').order_by('-price')
            paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
            page_number = request.GET.get('page', None)
            page_object = paginator.get_page(page_number)

            ads = []
            for ad in page_object:
                ads.append(
                    {
                        'id': ad.id,
                        'name': ad.name,
                        'author_id': ad.author_id,
                        'author': ad.author.first_name,
                        'price': ad.price,
                        'description': ad.description,
                        'is_published': ad.is_published,
                        'category_id': ad.category_id,
                        'image': ad.image.url if ad.image else None,
                    }
                )

            response = {
                'items': ads,
                'num_pages': paginator.num_pages,
                'total': paginator.count,
            }

            return JsonResponse(response, safe=False)

class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer


class AdListView(generics.GenericAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    name = 'Ad List'
    filter_backends = (DjangoFilterBackend,)

    def get(self, request):
        categories = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(instance=categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
