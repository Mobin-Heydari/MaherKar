from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Province, City




class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name', 'slug')

    def create(self, validated_data):
        # Extract the name from the validated data.
        name = validated_data.get('name')
        # Generate a slug using the name.
        slug = slugify(name, allow_unicode=True)
        # Create the province using keyword arguments.
        province = Province.objects.create(name=name, slug=slug)
        return province

    def update(self, instance, validated_data):
        # Use the new name if provided; otherwise, keep the current one.
        instance.name = validated_data.get('name', instance.name)
        # Update the slug based on the (new) name.
        instance.slug = slugify(instance.name, allow_unicode=True)
        instance.save()
        return instance


class CitySerializer(serializers.ModelSerializer):
    # Nested read-only representation of the related Province.
    province_detail = ProvinceSerializer(source='province', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'slug', 'province_detail')

    def create(self, validated_data):
        
        # Expect a 'province_slug' in the serializer context.
        province_slug = self.context.get('province_slug')
        if not province_slug:
            raise serializers.ValidationError({"province_slug": "Slug of the province is required."})
        
        # Retrieve the corresponding Province instance (or raise 404).
        province = get_object_or_404(Province, slug=province_slug)
        # Get the city name from the validated data.
        name = validated_data.get('name')
        # Generate a slug from the city name.
        slug = slugify(name, allow_unicode=True)
        # Create the City instance, linking it to the found Province.
        city = City.objects.create(province=province, name=name, slug=slug)
        return city

    def update(self, instance, validated_data):
        # Check if a new province slug is provided in the context.
        province_slug = self.context.get('province_slug')
        if province_slug:
            province = get_object_or_404(Province, slug=province_slug)
            instance.province = province

        # Update the city name, falling back to the current value if not provided.
        instance.name = validated_data.get('name', instance.name)
        # Update the slug based on the updated name.
        instance.slug = slugify(instance.name, allow_unicode=True)
        instance.save()
        return instance
