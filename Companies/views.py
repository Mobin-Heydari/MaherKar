from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsAdminOrOwnerForUpdateAndEmployerForCreate


class CompanyViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IsAdminOrOwnerForUpdateAndEmployerForCreate]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        """List all companies.
           دریافت لیست تمامی شرکت‌ها.
        """
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Company, id=pk)
        serializer = CompanySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Company created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        """Update an existing company.
           به‌روزرسانی اطلاعات یک شرکت موجود بر اساس اسلاگ.
        """
        instance = get_object_or_404(Company, id=pk)
        serializer = CompanySerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)