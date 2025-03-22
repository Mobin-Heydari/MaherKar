from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer



class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """List all companies."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug, *args, **kwargs):
        """Retrieve a specific company by its slug."""
        instance = get_object_or_404(Company, slug=slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new company. Employer field is auto-assigned."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Pass employer_id through serializer context
            serializer.save(employer_id=request.user.id)
            return Response({'Message': 'Company created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing company."""
        instance = get_object_or_404(Company, slug=slug)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
