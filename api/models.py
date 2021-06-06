from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.



class Image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = TaggableManager()
    description = models.CharField(max_length=200,default='')
    photo = models.CharField(max_length=256,null=False)
    published_on = models.DateTimeField('date ordered',default=timezone.now)
    location = models.CharField(max_length=256,default="")
    likes = models.IntegerField(default=0)
    delete_url =  models.CharField(max_length=256,default="")

    def get_absolute_url(self):
        return "/image/%i" % self.id

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'image')

class Collection(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=250,default='')
    private = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)

class Follower(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="followers")

    def __str__(self):
        return self.user.username