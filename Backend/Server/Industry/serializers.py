from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Industry, IndustryCategory, Skill



class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory
        fields = [
            'id',
            'name',
            'slug',
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        """
        Create a new Category instance.
        """
        # Auto-generate slug handled in the model's save() method
        name = validated_data.get('name')

        category = IndustryCategory.objects.create(name=name)
        return category

    def update(self, instance, validated_data):
        """
        Update an existing Category instance.
        """
        # Update fields
        instance.name = validated_data.get('name', instance.name)

        # Save changes
        instance.save()
        return instance



class IndustrySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Industry
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'category_name'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        """
        Create a new Industry instance by associating with an existing category using its slug.
        """
        # Extract category slug from the context
        category_slug = self.context.get('category_slug')
        if not category_slug:
            raise serializers.ValidationError({"category_slug": "Slug of the category is required."})
        
        # Retrieve the category using the slug
        category = get_object_or_404(IndustryCategory, slug=category_slug)

        # Create the industry with the retrieved category
        industry = Industry.objects.create(
            name=validated_data.get('name'),
            category=category,
        )
        return industry

    def update(self, instance, validated_data):
        """
        Update an existing Industry instance.
        """
        # Update fields
        instance.name = validated_data.get('name', instance.name)

        # Save changes
        instance.save()
        return instance


class SkillSerializer(serializers.ModelSerializer):
    # Nest the industry details in the Skill representation.
    industry = IndustrySerializer(read_only=True)
    
    class Meta:
        model = Skill
        fields = ('id', 'name', 'icon', 'industry')

    def create(self, validated_data):
       # Extract industry slug from the context
        industry_slug = self.context.get('industry_slug')
        if not industry_slug:
            raise serializers.ValidationError({"industry_slug": "Slug of the industry is required."})
        
        # Retrieve the industry using the slug
        industry = get_object_or_404(Industry, slug=industry_slug)

        skill = Skill.objects.create(
            name=validated_data.get('name'),
            icon=validated_data.get('icon'),
            industry=industry
        )

        skill.save()

        return skill
    


    def update(self, instance, validated_data):
        """
        Update an existing Industry instance.
        """
        
        # Extract industry slug from the context
        if industry_slug:
            industry_slug = self.context.get('industry_slug')
            industry = get_object_or_404(Industry, slug=industry_slug)
            instance.industry = industry

        # Update fields
        instance.name = validated_data.get('name', instance.name)

        # Save changes
        instance.save()
        return instance
