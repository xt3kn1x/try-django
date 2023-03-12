from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from .utils import slugify_instance_title


# Create your models here.

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none() # Again, if nothing, return nothing - empty set []
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups) # return the filtered query sets based upon lookups conditions


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db) # ??
    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now, null=True, blank=True)
    objects = ArticleManager()

    def get_absolute_url(self):
        # return f'{self.slug}'
        return reverse("article-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # if self.slug is None:
        #     self.slug = slugify(self.title)
        super().save(*args, **kwargs)



def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    # print(args, kwargs)
    # print('sender and instance')
    # print(sender, instance)
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    # print(args, kwargs)
    # print('sender, instance, and created')
    # print(sender, instance,created)
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)