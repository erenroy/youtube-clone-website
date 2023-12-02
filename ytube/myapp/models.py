from django.db import models
from django.contrib.auth.models import User
# Create your models here.

CATEGORY_CHOICES = (
    ('X' , 'Action'),
    ('AN' , 'Animes'),
    ('K' , 'Film'),
    ('G' , 'Gaming'),
    ('L' , 'Learing'),
    ('F' , 'Fashion'),
    ('S' , 'Sports'),
)

class ChannelsForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc =  models.TextField()
    content = models.CharField(max_length=255)
    channelimages = models.ImageField(upload_to='cimg')
    channelthumbles = models.ImageField(upload_to='timg')
    subscibers = models.IntegerField(default=0)

     # Add other fields for your form data

    def __str__(self):
        return self.user.username

class ChannelVideo(models.Model):
    
    videotitle = models.CharField(max_length=255)
    videodesc =  models.CharField(max_length=455)
    channelimages = models.ImageField(upload_to='videosimage')
    channelthumbles = models.FileField(upload_to='videos')
    videodate = models.DateTimeField(auto_now_add=True)
    smallimage = models.ImageField(upload_to='smallchannelimage')
    channelname = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=25,default='A')
    slug = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Subscription(models.Model):
    channelsubscribers = models.ForeignKey(ChannelsForm, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriber_count = models.IntegerField(default=0)

    def str(self):
        return self.user.username

class Comment(models.Model):
    video = models.ForeignKey(ChannelVideo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    movie = models.ForeignKey(ChannelVideo,on_delete=models.CASCADE)


class Shorts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shortvideo = models.FileField(upload_to='shortsvideos')
    shortchannelname = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class CommunitymPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compost = models.FileField(upload_to='comupost')
    comtitle = models.CharField(max_length=255)
    comchannelname = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

