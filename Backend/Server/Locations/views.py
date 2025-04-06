from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .permissions import IsAdminUserOrReadOnly
from .models import Province, City
from .serializers import ProvinceSerializer, CitySerializer



class ProvinceViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and destroying Province instances.
    Only admin users may perform create, update, or delete operations.
    """
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        province = get_object_or_404(Province, slug=slug)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can create data.")
        serializer = ProvinceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This calls your serializer's create() method.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update data.")
        province = get_object_or_404(Province, slug=slug)
        serializer = ProvinceSerializer(province, data=request.data)
        if serializer.is_valid():
            serializer.save()  # This calls your serializer's update() method.
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete data.")
        province = get_object_or_404(Province, slug=slug)
        province.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and destroying City instances.
    The city serializer expects a 'province_slug' via context,
    and only admin users may modify data.
    """
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        city = get_object_or_404(City, slug=slug)
        # The context here can be empty or include additional info if needed.
        serializer = CitySerializer(city, context={})
        return Response(serializer.data)

    def create(self, request, province_slug):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can create data.")
        province = get_object_or_404(Province, slug=province_slug)
        # Pass 'province_slug' from the request data into the serializer context.
        serializer = CitySerializer(data=request.data, context={'province_slug': province.slug})
        if serializer.is_valid():
            serializer.save()  # Calls CitySerializer.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update data.")
        city = get_object_or_404(City, slug=slug)
        serializer = CitySerializer(
            city, 
            data=request.data, 
            context={'province_slug': request.data.get('province_slug')}
        )
        if serializer.is_valid():
            serializer.save()  # Calls CitySerializer.update()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete data.")
        city = get_object_or_404(City, slug=slug)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
