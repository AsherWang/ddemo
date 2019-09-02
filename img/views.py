from rest_framework import viewsets, status
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