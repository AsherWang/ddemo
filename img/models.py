from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

def check_used_info(a, b):
    return a.id == b.id and a.type == b.type and a.field == b.field

class Image(models.Model):
    md5 = models.TextField(null=False, blank=False)
    source = models.ImageField(upload_to='images')
    thumbnail = ImageSpecField(
        source='source',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60})
    normal = ImageSpecField(
        source='source',
        processors=[ResizeToFill(1920, 1080)],
        format='JPEG',
        options={'quality': 60})
    '''
    used_by is a collection of used_info
    used_info is a json value like {'type': modelName, 'id': modelId, 'field': modelField}
    '''
    used_by = ArrayField(JSONField(null=False, blank=False), null=True, blank=False)
    def index_used_info(self, used_info):
        return next((i for i,item in enumerate(self.used_by) if check_used_info(item, used_info)), -1)
   
    def add_used_info(self, used_info):
        pre_instance = Image.objects.get(id=self.id)
        if pre_instance.index_used_info(used_info) == -1:
            self.used_by = pre_instance.used_by
            self.used_by.push(used_info)

    def remove_used_info(self, used_info):
        index = self.index_used_info(used_info)
        if(index != -1):
            del self.used_by[index]




class AlbumMixin(models.Model):
    images_ids =  ArrayField(models.PositiveIntegerField(null=False, blank=False),null=True, blank=False)

    # for serializer to fetch url
    def get_images(self):
        if(self.images_ids is None):
            return None
        else:
            return Image.objects.filter(id__in=self.images_ids)
    
    def get_used_info(self):
        return {'id': self.id, 'type': self.__class__.__name__, 'field': 'images_ids'}
    # may be not used frequently
    def rewrite_images_rel(self):
        used_info = self.get_used_info()
        for img in self.get_images():
            img.add_used_info(used_info)
    class Meta:
        abstract = True

class Article(AlbumMixin):
    title = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title