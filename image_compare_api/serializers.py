from rest_framework import serializers
from .models import ImageCompare

class ImageCompareSerializer(serializers.ModelSerializer):
    published = serializers.BooleanField(default=True)

    class Meta:
        model = ImageCompare
        fields = ('pk', 'image', 'published', 'created_at')
