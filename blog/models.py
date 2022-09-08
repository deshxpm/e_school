from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from classroom.models import Category

USER=settings.AUTH_USER_MODEL




class Image(models.Model):
    image=models.ImageField(upload_to='blog_images')


# class Category(models.Model):
#     name=models.CharField(max_length=10,default='Cat')
#
#     def __str__(self):
#         return self.name

    # def get_absolute_cat_url(self):
    #     return reverse('cat-detail',kwargs={'id':self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=10, default='Tag')

    def __str__(self):
        return self.name

    # def get_absolute_tag_url(self):
    #     return reverse('tag-detail',kwargs={'id':self.pk})

class PostAuthor(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100,default='Title')
    sub_title = models.CharField(max_length=100,default='SubTitle',blank=True,null=True)
    content=models.TextField(default="The Content")
    date_posted = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(PostAuthor, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag,blank=True)
    cat=models.ManyToManyField(Category,blank=True)
    thumbnail = models.ImageField(upload_to='blog_images',blank=True,null=True)
    images=models.ManyToManyField(Image,blank=True)
    is_like=models.ManyToManyField(USER,blank=True,related_name="user_likes")
    is_save=models.ManyToManyField(USER,blank=True,related_name="user_save")

    def __str__(self):
        return self.title

    def get_blog_absolute_url(self):
        return reverse('blog_details',kwargs={'id':self.pk})

def validate_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")