from cms import models as CM
from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry

class GeoFieldHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, instance):
        """Convert `geom` to GeoJSON."""
        ret = super().to_representation(instance)
        ret['geom'] = ret['geom'] and GEOSGeometry(ret['geom']).json
        return ret
    def to_internal_value(self, data):
        """Convert `geom` from GeoJSON to value saving in db."""
        ret = super().to_internal_value(data)
        ret['geom']=ret['geom'] and GEOSGeometry(ret['geom'], srid=4326).ewkt
        return ret

class StatusSerializer:
    status_display = serializers.SerializerMethodField()
    def get_status_display(self, instance):
        return instance.status_display

class CountrySerializer(GeoFieldHyperlinkedModelSerializer):
    class Meta:
        model = CM.Country
        fields = (
            'id',
            'url',
            'code',
            'name_en',
            'full_description_en',
            # 'coords',
            'classification',
            'classification_display',
            'geom',
            'created',
            'edited',
        )
class AdminFifthLvlSerializer(GeoFieldHyperlinkedModelSerializer):
    class Meta:
        model = CM.AdminFifthLvl
        fields = (
            'id',
            'name_en',
            'geom'
        )
class AdminFirstLvlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CM.AdminFirstLvl
        fields = (
            'id',
            'status_display',
            'name_en',
            'name_cn',
            'name_it',
            'name_es',
            'name_fr',
            'name_el',
            'name_nl',
            'name_de',
        )
class AdminFirstLvlDetailedSerializer(GeoFieldHyperlinkedModelSerializer,StatusSerializer):
    class Meta:
        model = CM.AdminFirstLvl
        # fields = '__all__'
        exclude = ['creator','last_editor']

class POICategorySerializer(serializers.HyperlinkedModelSerializer):
    # id is not included in '__all__'
    id = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    def get_id(self, instance):
        return instance.id
    def get_status_display(self, instance):
        return instance.status_display
    class Meta:
        model = CM.POICategory
        fields = '__all__'

class POITypeSerializer(serializers.HyperlinkedModelSerializer):
    # id is not included in '__all__'
    id = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    def get_id(self, instance):
        return instance.id
    def get_status_display(self, instance):
        return instance.status_display
    class Meta:
        model = CM.POIType
        fields = '__all__'

# FIXME:when using serializers.HyperlinkedModelSerializer
# sub_categories is required to be an array with urls of sub_category when creating a poi record
class POISerializer(serializers.ModelSerializer):
    # id is not included in '__all__'
    id = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    def get_id(self, instance):
        return instance.id
    def get_status_display(self, instance):
        return instance.status_display
    class Meta:
        model = CM.POI
        # fields = '__all__'
        exclude = ['creator','last_editor']

