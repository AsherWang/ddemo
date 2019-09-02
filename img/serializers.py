from img import models as CM
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    def get_images(self, instance):
        imgs = instance.get_images()
        if imgs is None:
            return None
        return [ x.source.url for x in instance.get_images()]
    class Meta:
        model = CM.Article
        fields = ['id','title','images', 'images_ids']
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CM.Image
        fields = ['id','md5','source','used_by']

