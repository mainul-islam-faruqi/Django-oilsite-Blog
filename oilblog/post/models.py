from django.db.models import Q
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from django.db.models.signals import pre_save, post_save
# from oilblog.utils import unique_slug_generator

User = get_user_model()

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length = 30)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE,
                            related_name='comments')
    approve_comment = models.BooleanField(default=False)
    def approve(self):
        self.approve_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.content



class PostQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)
        
class PostManager(models.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
        
    def get_by_id(self, id):
        # return self.get_queryset().filter(id=id)  # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()  # individual Object  
        return None

#     def search(self,query):
#         lookups = (Q(title__icontains=query)|
#                     Q(overview__icontains=query)|
#                     Q(author__icontains=query)
#         )
#         return self.get_queryset().filter(lookups).distinct()

class Post(models.Model):
    title = models.CharField(max_length=150)
    # slug = models.SlugField(max_length=150,blank=True,unique=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add= True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    incredient_pdf = models.ImageField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    objects = PostManager()

  
    def total_likes(self):
        return self.likes.all().count()

    def __str__(self):
        return str(self.pk)
    
    
    def get_absolute_url(self, **kwargs):
        return "/post/{pk}/".format(pk=self.pk)
        
        
    def get_category_count(self):
        return self.categories.all().count()

    def approve_comments(self):
        return self.comments.filter(approve_comment=True)

    def comment_count(self):
        return Comment.objects.filter(post=self).count()

# def post_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)

# pre_save.connect(post_pre_save_receiver, sender=Post)

