from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from img import serializers as CS
from img import models as CM

# previous api for upload an image for tinymce
# test upload api
# upload the image file to s3 and get a url and then return
# class ImageUpload(APIView):
#     def post(self, request, format=None):
#         # get file from request.data.file
#         # file = request.data.get('file') #django.core.files.uploadedfile.InMemoryUploadedFile
#         # fileContent = file.read() #bytes
#         return Response(
#             status=status.HTTP_200_OK,
#             data={ "location": "http://placekitten.com/200/300"}
#         )

class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed o edited.
    """
    queryset = CM.Article.objects.all().order_by('id')
    serializer_class = CS.ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact']
    }

    # @action(detail=True, methods=['post'])
    # def add_image(self, request, pk=None):
    #     article = self.get_object()
    #     img_id = request.data['img_id']
    #     serializer = CS.ImageSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # create or find a existed one
    #         md5_str = serializer.validated_data.get('md5')
    #         new_img = CM.Image.objects.filter(md5=md5_str)
    #         if(not new_img):
    #             new_img = serializer.create(serializer.validated_data)
    #         else:
    #             new_img = new_img[0]
    #         article.add_image(new_img)
    #         article.save()
    #         return Response({'status': 'img added'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        article = self.get_object()
        image_id = request.data['image_id']
        img = CM.Image.objects.filter(id=image_id)
        if(img):
            img = img[0]
            article.add_image(img)
            article.save()
            return Response({'status': 'img added'})
        else:
            return Response('no image with id %s found' % image_id, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_image(self, request, pk=None):
        article = self.get_object()
        image_id = request.data['image_id']
        img = CM.Image.objects.filter(id=image_id)
        if(img):
            img = img[0]
            print(img.id)
            article.remove_image(img)
            article.save()
            return Response({'status': 'img removed'})
        else:
            return Response('no image with id %s found' % image_id, status=status.HTTP_404_NOT_FOUND)



class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed o edited.
    """
    queryset = CM.Image.objects.all().order_by('id')
    serializer_class = CS.ImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact']
    }