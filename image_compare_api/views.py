from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ImageCompare
from .serializers import ImageCompareSerializer


class ImageData(APIView):
    """
    List all images, or create a new image.
    """
    def get(self, request, format=None):
        image = ImageCompare.activated.all()
        serializer = ImageCompareSerializer(image, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Curl to test, use:
        curl -F "image=@/home/.../your-image.jpg" 127.0.0.1:8000
        """
        serializer = ImageCompareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageItem(APIView):
    """
    Retrieve a image instance.
    """
    def get_object(self, pk):
        try:
            return ImageCompare.activated.get(pk=pk)
        except ImageCompare.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageCompareSerializer(image)
        return Response(serializer.data)
