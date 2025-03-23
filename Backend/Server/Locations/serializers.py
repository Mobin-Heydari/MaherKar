from rest_framework import serializers
from .models import Province, City




class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name', 'slug')


class CitySerializer(serializers.ModelSerializer):
    # Allow clients to specify/update the province using its primary key;
    # also provide a nested representation of the province.
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    province_detail = ProvinceSerializer(source='province', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'slug', 'province', 'province_detail')
