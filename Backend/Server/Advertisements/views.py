from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404

from .models import Advertisement, Application
from .serializers import AdvertisementSerializer, ApplicationSerializer




class AdvertisementViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Advertisement.objects.all()
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
        query = get_object_or_404(Advertisement, slug=slug)
        serializer = AdvertisementSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, slug):
        query = get_object_or_404(Advertisement, slug=slug)
        serializer = AdvertisementSerializer(query, data=request.data, partial=True)
        if request.user == query.owner or request.user.is_staff:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'Message': "Advertisemenet updated.",
                        "Data": serializer.data
                    }, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "You dont have permission"}, status=status.HTTP_403_FORBIDDEN)



class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Application model operations.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Automatically handles job seeker linkage in the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)