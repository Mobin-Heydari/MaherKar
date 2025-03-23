from rest_framework import serializers
from .models import Industry, IndustryCategory  # Make sure to update the import for Category



class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory
        fields = [
            'id',
            'name',
            'slug',
            'description'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        """
        Create a new Category instance.
        """
        # Auto-generate slug handled in the model's save() method
        name = validated_data.get('name')
        description = validated_data.get('description', '')

        category = IndustryCategory.objects.create(
            name=name,
            description=description
        )
        return category

    def update(self, instance, validated_data):
        """
        Update an existing Category instance.
        """
        # Update fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # Save changes
        instance.save()
        return instance


class IndustrySerializer(serializers.ModelSerializer):
    category = IndustryCategorySerializer()  # Use the complete Category representation

    class Meta:
        model = Industry
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'description'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        """
        Create a new Industry instance with a nested category.
        """
        # Extract category data
        category_data = validated_data.pop('category')
        
        # Ensure the category exists or create it
        category, _ = IndustryCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={'description': category_data.get('description', '')}
        )

        # Create the industry
        industry = Industry.objects.create(
            category=category,
            **validated_data
        )
        return industry

    def update(self, instance, validated_data):
        """
        Update an existing Industry instance and its category.
        """
        # Extract category data
        category_data = validated_data.pop('category', None)
        
        # Update or create category if data is provided
        if category_data:
            category, _ = IndustryCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data.get('description', '')}
            )
            instance.category = category

        # Update other Industry fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # Save the instance
        instance.save()
        return instance
