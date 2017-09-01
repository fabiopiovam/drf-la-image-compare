from django.conf.urls import url

from .views import ImageData, ImageItem

app_name = 'image_compare_api'

urlpatterns = [

    # IMAGES

    # /
    url(r'^$', ImageData.as_view(), name='image-data'),

    # /1
    url(r'^(?P<pk>[0-9]+)/$', ImageItem.as_view(), name='image-item'),
]
