import uuid
import os
import glob

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from .validators import FileValidator


class ImageCompareActivatedManager(models.Manager):
    ''' Activated records '''

    def get_queryset(self):
        return super().get_queryset().filter(
            published=True).order_by('id')


class ImageCompare(models.Model):

    def get_upload_to_image(self, filename):
        ext = filename[-3:].lower()
        if ext == 'peg':
            ext = 'jpeg'

        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('image_compare/to_compare', filename)

    image = models.ImageField('Imagem', upload_to=get_upload_to_image,
                              validators=[FileValidator(
                                  max_size=1 * 1024 * 1024)],
                              help_text=_('''Selecione a imagem de
                               exemplo da certidão, normalmente nos formatos
                               jpg, png, gif, etc.'''))
    published = models.BooleanField(u'Publicado', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ''' Managers '''
    objects = models.Manager()
    activated = ImageCompareActivatedManager()

    class Meta:
        ordering = ['id']
        verbose_name = _('imagem')
        verbose_name_plural = _('imagens')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'id': self.id}
        return reverse('image_compare_api:image-data', kwargs=kwargs)

    def save(self, *args, **kwargs):
        if self.id:
            ''' delete old image if its changed '''
            obj = ImageCompare.objects.get(id=self.id)
            if obj.image and self.image not in [obj.image]:
                for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,
                                                obj.image)):
                    os.remove(fl)

        super().save(*args, **kwargs)

    def delete(self):
        ''' delete image file '''

        obj = ImageCompare.objects.get(id=self.id)
        super().delete()

        if obj.image:
            for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,
                                            obj.image)):
                os.remove(fl)
