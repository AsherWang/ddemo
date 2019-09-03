from img import models as CM
from rest_framework import serializers
from hashlib import md5

def get_file_hash(file):
    hasher = md5()
    buf = file.read()
    hasher.update(buf)
    return hasher.hexdigest()

class ImageSerializer(serializers.ModelSerializer):
    # thumbnail = serializers.ImageField()
    class Meta:
        model = CM.Image
        fields = ['id','md5','source','used_by']
    def to_representation(self, instance):
        """thumbnail"""
        ret = super().to_representation(instance)
        ret['thumbnail'] = instance.thumbnail.url
        return ret
    def to_internal_value(self, data):
        """calc md5 for img"""
        ret = super().to_internal_value(data)
        if(ret['source'] != None):
            ret['md5'] = get_file_hash(ret['source'])
        return ret


class AlbumSerializerMixin(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    def get_images(self, instance):
        imgs = instance.get_images()
        if imgs is None:
            return None
        return [ x.source.url for x in instance.get_images()]

class ArticleSerializer(AlbumSerializerMixin):
    class Meta:
        model = CM.Article
        fields = ['id','title','images', 'images_ids']

