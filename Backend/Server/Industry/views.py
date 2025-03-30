from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import IndustryCategory, Industry
from .serializers import IndustryCategorySerializer, IndustrySerializer





class IndustryCategoryViewSet(ModelViewSet):
    """
    ViewSet for managing Industry Categories.
    """
    queryset = IndustryCategory.objects.all()
    serializer_class = IndustryCategorySerializer, IndustrySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """List all categories."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug, *args, **kwargs):
        """Retrieve a specific category by its slug."""
        instance = get_object_or_404(IndustryCategory, slug=slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new category."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Category created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing category."""
        instance = get_object_or_404(IndustryCategory, slug=slug)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class IndustryViewSet(ModelViewSet):
    """
    ViewSet for managing Industries.
    """
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """List all industries."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug, *args, **kwargs):
        """Retrieve a specific industry by its slug."""
        instance = get_object_or_404(Industry, slug=slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new industry. Requires category slug."""
        category_slug = request.data.get('category_slug')
        if not category_slug:
            return Response(
                {'Error': 'category_slug is required for creating an industry.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data, context={'category_slug': category_slug})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Industry created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing industry."""
        instance = get_object_or_404(Industry, slug=slug)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SkillViewSet(ModelViewSet):
    """
        ViewSet for managing Industries.
    """
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """List all industries."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug, *args, **kwargs):
        """Retrieve a specific industry by its slug."""
        instance = get_object_or_404(Industry, slug=slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new industry. Requires industry slug."""
        industry_slug = request.data.get('industry_slug')
        if not industry_slug:
            return Response(
                {'Error': 'industry_slug is required for creating an industry.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data, context={'industry_slug': industry_slug})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Industry created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing industry."""
        instance = get_object_or_404(Industry, slug=slug)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)