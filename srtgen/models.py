from django.db import models
from users.models import AuthUser 
from django.core.validators import FileExtensionValidator
# Create your models here.
#
class Srtgen(models.Model):
    link=models.URLField()
    title=models.CharField(max_length=1000)
    user=models.ForeignKey(AuthUser,on_delete=models.CASCADE)
    preview=models.FileField(upload_to='previews_uploaded',null=True,blank=True,
validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    video=models.FileField(upload_to='videos_uploaded',null=True,blank=True,
validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    file=models.FileField(upload_to="srt_uploaded",null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['srt'])])
    public = models.BooleanField(default=True)
    duration = models.FloatField(default=0)
    def __str__(self) -> str:
        return self.title
class Favourites(models.Model):
    user=models.ForeignKey(AuthUser,on_delete=models.CASCADE)
    link=models.ForeignKey(Srtgen,on_delete=models.CASCADE)

    