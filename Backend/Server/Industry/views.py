from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import IndustryCategory, Industry, Skill
from .serializers import IndustryCategorySerializer, IndustrySerializer, SkillSerializer





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
        if request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Category created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing category."""
        if request.user.is_staff:
            instance = get_object_or_404(IndustryCategory, slug=slug)
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, name):
        """Delete the existing category"""
        if request.user.is_staff:
            category = get_object_or_404(IndustryCategory, name=name)
            self.perform_destroy(category)
            return Response({"Massage": "The category deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "Only admin users can dele datas"}, status=status.HTTP_403_FORBIDDEN)




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

    def create(self, request, category_slug, *args, **kwargs):
        """Create a new industry. Requires category slug."""

        if request.user.is_staff:
            if not category_slug:
                return Response({'Error': 'category_slug is required for creating an industry.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data, context={'category_slug': category_slug})
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Industry created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, slug, *args, **kwargs):
        """Update an existing industry."""
        if request.user.is_staff:
            instance = get_object_or_404(Industry, slug=slug)
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, slug):
        """Delete the existing industry"""
        if request.user.is_staff:
            industry = get_object_or_404(Industry, slug=slug)
            self.perform_destroy(industry)
            return Response({"Massage": "The industry deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "Only admin users can dele datas"}, status=status.HTTP_403_FORBIDDEN)



class SkillViewSet(ModelViewSet):
    """
        ViewSet for managing Industries.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """List all industries."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, name, *args, **kwargs):
        """Retrieve a specific industry by its name."""
        instance = get_object_or_404(Skill, name=name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, industry_slug, *args, **kwargs):
        """Create a new industry. Requires industry slug."""
        if request.user.is_staff:
            if not industry_slug:
                return Response({'Error': 'Skill is required for creating an industry.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data, context={'industry_slug': industry_slug})
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Skill created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, name, *args, **kwargs):
        """Update an existing industry."""

        if request.user.is_staff:
            instance = get_object_or_404(Skill, name=name)
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Massage": "Only admin users can write datas"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, name):
        """Delete the existing skill"""
        if request.user.is_staff:
            skill = get_object_or_404(Skill, name=name)
            self.perform_destroy(skill)
            return Response({"Massage": "The skill deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Massage": "Only admin users can dele datas"}, status=status.HTTP_403_FORBIDDEN)