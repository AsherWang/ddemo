from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django_s3_storage.storage import S3Storage

storage = S3Storage()

class Image(models.Model):
    md5 = models.TextField(null=False, blank=True)
    source = models.ImageField(upload_to='images', storage=storage)
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
    used_by = ArrayField(JSONField(null=False, blank=False), null=False, blank=False, default=list)
    def index_used_info(self, used_info):
        return next((i for i,item in enumerate(self.used_by) if item == used_info), -1)
    def add_used_info(self, used_info):
        if self.index_used_info(used_info) == -1:
            self.used_by.append(used_info)
            self.save()
    def remove_used_info(self, used_info):
        index = self.index_used_info(used_info)
        if(index != -1):
            del self.used_by[index]
            self.save()


class AlbumMixin(models.Model):
    images_ids =  ArrayField(models.PositiveIntegerField(null=False, blank=False),null=False, blank=False, default=list)

    # for serializer to fetch url
    def get_images(self):
        return Image.objects.filter(id__in=self.images_ids)
    
    def get_used_info(self):
        return {'id': self.id, 'type': self.__class__.__name__, 'field': 'images_ids'}
    def index_image(self, img):
        return next((i for i,img_id in enumerate(self.images_ids) if img_id == img.id), -1)
    def rewrite_images_rel(self):
        used_info = self.get_used_info()
        for img in self.get_images():
            img.add_used_info(used_info)
    def add_image(self,img):
        if(self.index_image(img) == -1):
            self.images_ids.append(img.id)
            img.add_used_info(self.get_used_info())
    def remove_image(self,img):
        index = self.index_image(img)
        if(index == -1):
            return
        del self.images_ids[index]
        img.remove_used_info(self.get_used_info())
        self.save()
    class Meta:
        abstract = True

class Article(AlbumMixin):
    title = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title