import uuid

from django.db import models

# Create your models here.
from django.conf import settings

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    file = models.FileField(verbose_name="CSV File", upload_to='csv_files/')
    file_description = models.TextField("CSV File Description")
    slug = models.SlugField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.user == None:
            return self.file.url
        return f'{self.user.username} === {self.file.url}'


    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = str(uuid.uuid4()).replace('-','')[:9]
        super().save(*args, **kwargs)


#return ("{} ({} {})".format(self.user.email, self.user.first_name, self.user.last_name))
