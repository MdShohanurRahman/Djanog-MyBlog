from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify



# Create your models here.


class PublishedManager(models.Manager):
    """
    custom model manager.filtering which status is =published
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Category(models.Model):
    """
    many to many relation with posts
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    thumbnail = models.ImageField(upload_to='images/category', blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    many to many relation with posts
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)

    def __str__(self):
        return self.name
    


class Post(models.Model):
    """
    post model with different relationship
    """
    objects = models.Manager() #our default manager
    published = PublishedManager() #our custom manager
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    description = models.TextField(blank=True, null=True)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='images/post', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    restrict_comment= models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'id': self.id, 'slug': self.slug})


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug



class Comment(models.Model):
    """
    user commenting system and reply
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self',on_delete=models.CASCADE, null=True, related_name='replies')
    content = RichTextUploadingField(blank=True, null=True, config_name='special')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title + ' by' + self.user.username

